/*
	Simple Zone Allocator
	Author: peter
*/

#include <sys/mman.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>
#include <time.h>
#include "libzone.h"
#include "bltree.h"

zone_hastable_t zone_table;
uint64_t        cookie[2];

void constructor() __attribute__((constructor));
void destructor() __attribute__((destructor));

void zone_table_init();
void zone_table_deinit();
void zone_init(zone_t zone, const char *zone_name, size_t object_size, uint8_t is_mapped);
void zone_destroy(zone_t zonep);

void zone_create_internal(const char *zone_name, size_t object_size, uint8_t is_mapped);
void* zone_alloc_internal(const char *zone_name);
void zone_free_internal(const char *zone_name, void *ptr);

size_t round_up(size_t size, size_t base)
{
	return size % base == 0 ? size : base + (size / base) * base;
}

#define CHUNK_COOKIE_PTR(chunkptr, object_size) (void *)((uint8_t *)chunkptr + object_size)
#define PAGEMAP_COOKIE_PTR(pagep) (void *)((uint8_t *)pagep + sizeof(struct page_mapped) + \
							round_up(pagep->mapped_capacity, BIT_ARRAY_SIZE) / BIT_PER_BYTE)

#define BLNODE_AS_ZONE(bl_node_p) BLTNODE_AS_OBJECT(bl_node_p, blnode, struct zone)
#define ZONE_AS_BLNODE(zonep)  OBJECT_AS_BLTNODE(zonep, blnode, struct zone)

int zone_name_cmp(BLNode_t node1, BLNode_t node2)
{
	zone_t zone1, zone2;

	if(!node1 && !node2)
		return 0;

	if(!node1)
		return -1;

	if(!node2)
		return 1;

	zone1 = BLNODE_AS_ZONE(node1);
	zone2 = BLNODE_AS_ZONE(node2);

	return strncmp(zone1->zone_name, zone2->zone_name, sizeof(zone1->zone_name) - 1);
}

void blnode_zone_destroy(BLNode_t node)
{
	if(!node)
		return;
	zone_destroy(BLNODE_AS_ZONE(node));
}

#define ZONE_BLTREE_INSERT(root, a_node) (BLNODE_AS_ZONE(BLTInsert(ZONE_AS_BLNODE(root), \
													ZONE_AS_BLNODE(a_node), zone_name_cmp)))
#define ZONE_BLTREE_DESTROY(root) \
		BLTDestroy(ZONE_AS_BLNODE(root), blnode_zone_destroy)

#define ZONE_HAS_CHILD(zone) (BLNHEIGHT(ZONE_AS_BLNODE(zone)) != 0)

zone_t zone_bltree_search(zone_t root, const char *zone_name)
{
	struct zone tmp_zone;
	BLNode_t match_node;

	bzero((void *)&tmp_zone, sizeof(struct zone));
	strncpy(tmp_zone.zone_name, zone_name, sizeof(tmp_zone.zone_name) - 1);

	match_node = BLTSearch(ZONE_AS_BLNODE(root), ZONE_AS_BLNODE(&tmp_zone), zone_name_cmp);
	if(match_node){
		return BLNODE_AS_ZONE(match_node);
	}

	return NULL;
}

void constructor()
{
	// init secure cookie to prevent heap overflow
#ifdef USECOOKIE
	FILE *fp;

	fp = fopen("/dev/urandom", "rb");
	if(fp){
		fread((char *)&cookie, 1, sizeof(cookie), fp);
		fclose(fp);

	} else {
		// use rand instead
		int *pcookie = (int *)&cookie;
		srand(time(NULL));
		pcookie[0] = rand();
		pcookie[1] = rand();
		pcookie[2] = rand();
		pcookie[3] = rand();
		
	}
	cookie[0] &= 0xFFFFFFFFFFFFFF00; // avoid leakage cookie
#endif
	// initialize zone_table when this shared library is loaded
	zone_table_init();
}
 
void destructor()
{
	zone_table_deinit();
}

size_t hash_string(const char *str)
{
	// hash calulation for zone_name
	size_t hash = 0;
	char *p;
	int i;

	for(i = 0, p = (char *)str; (p[0] != '\x00') && (i < MAX_NAME); p++, i++){
		hash += ((size_t)p[0]) * (10*(i + 1));
	}
	return hash;
}

uint64_t bitmap_find_idx(uint64_t *bitmap, int bitmap_size)
{
	uint64_t chunk_idx = -1LL;
	int i, k;
	int n_loop = round_up(bitmap_size, BIT_ARRAY_SIZE) / BIT_ARRAY_SIZE;

	for(i = 0; i < n_loop; i++){
		if(bitmap[i] & (uint64_t)(~0ULL)){
			// found suitable chunk
			for(k = 0; k < BIT_ARRAY_SIZE; k++){
				if(BIT64_IS_SET(bitmap[i], k)){
					chunk_idx = i*BIT_ARRAY_SIZE + k;
					break;
				}
			}
			break;
		}
	}

	return chunk_idx;
}

zone_t zone_table_get_zone(const char * zone_name)
{
	zone_t zone;
	uint32_t idx = 0;

	if(strncmp(Z_ZONE_BOOTSTRAP_NAME, zone_name, sizeof(Z_ZONE_BOOTSTRAP_NAME)) == 0){
		// return zone bootstrap
		return &(zone_table->zone_bootstrap);
	}

	idx  = hash_string(zone_name) % zone_table->capacity;
	zone = zone_table->zones[idx];
	
	if(!zone)
		return NULL;

	if(strncmp(zone->zone_name, zone_name, sizeof(zone->zone_name) - 1)){
		// search for other node in this zone tree
		return zone_bltree_search(zone, zone_name);
	}

	return zone;
}

page_mapped_t map_new_page(size_t object_size)
{
	size_t page_size;
	size_t n_object;
	size_t nbit_map;
	size_t size_page_mapped;
	page_mapped_t new_page;

	nbit_map = 0;
	n_object = MAX_PAGE_SIZE / object_size;
	if(n_object < MAX_OBJECT_PER_MAP)
		n_object = MAX_OBJECT_PER_MAP;

	nbit_map = round_up(n_object, BIT_ARRAY_SIZE) / BIT_PER_BYTE;

	size_page_mapped = sizeof(struct page_mapped) + nbit_map;
#ifdef USECOOKIE
	size_page_mapped += sizeof(cookie);
#endif

	page_size = round_up(size_page_mapped + n_object * object_size, MAX_PAGE_SIZE);
	new_page = (page_mapped_t)mmap(NULL, page_size, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
	if((int64_t)new_page == -1){
		return NULL;
	}

	bzero((void *)new_page, sizeof(struct page_mapped) + nbit_map);
	new_page->mapped_capacity = n_object;
	new_page->base_address = (void *)((uint8_t *)new_page + size_page_mapped);
	new_page->cur_address = new_page->base_address;

#ifdef USECOOKIE
	memcpy(PAGEMAP_COOKIE_PTR(new_page), (void *)&cookie, sizeof(cookie));
#endif
	return new_page;
}

int page_unmap_page(page_mapped_t unmap_page, size_t object_size)
{
	size_t page_size;
	size_t size_page_mapped;

#ifdef USECOOKIE
	if(memcmp(PAGEMAP_COOKIE_PTR(unmap_page), (void *)&cookie, sizeof(cookie))){
		fprintf(stderr, "Unmap malicious page, abort()\n");
		abort();
	}
#endif

	size_page_mapped = sizeof(struct page_mapped) + round_up(unmap_page->mapped_capacity, BIT_ARRAY_SIZE) / BIT_PER_BYTE;
#ifdef USECOOKIE
	size_page_mapped += sizeof(cookie);
#endif

	page_size = round_up(unmap_page->mapped_capacity * object_size + size_page_mapped, MAX_PAGE_SIZE);
	return munmap((void *)unmap_page, page_size);
}

#ifdef USEZMALLOC

#define MAX_MALLOC_SIZE_NAME (MAX_PAGE_SIZE * 2)/MIN_CHUNK_SIZE
#define MAX_MALLOC_NAME_LEN  64
static char z_malloc_zone_name[MAX_MALLOC_SIZE_NAME][MAX_MALLOC_NAME_LEN];

void zmalloc_init()
{
	char zone_name_buffer[MAX_MALLOC_NAME_LEN] = {0};
	uint32_t zone_chunk_size;
	uint32_t idx = 0;

	for(zone_chunk_size = MIN_CHUNK_SIZE; zone_chunk_size < MAX_PAGE_SIZE * 2; zone_chunk_size+= MIN_CHUNK_SIZE){
		snprintf(zone_name_buffer, sizeof(zone_name_buffer), "zmalloc.%d", zone_chunk_size);
		idx = (zone_chunk_size/MIN_CHUNK_SIZE) - 1;
		strncpy(&(z_malloc_zone_name[idx]), zone_name_buffer, sizeof(z_malloc_zone_name[idx]) - 1);
		zone_create_internal(zone_name_buffer, zone_chunk_size, 0);
	}
}
#endif

void zone_table_init()
{
	size_t map_size = round_up(sizeof(struct zone_hashtable) + DEFAULT_ZONE_SIZE * sizeof(zone_t), MAX_PAGE_SIZE);
	size_t zone_object_size;

	if(zone_table)
		return;

	zone_table = (zone_hastable_t)mmap(NULL, map_size, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0);
	if((int64_t)zone_table == -1LL){
		fprintf(stderr, "Unable to map zone_table\n");
		abort();
	}

	bzero((void *)zone_table, map_size);
	zone_table->capacity = DEFAULT_ZONE_SIZE;
	zone_table->num_zone = 0;

	zone_object_size = sizeof(struct zone);
#ifdef USECOOKIE
	zone_object_size += sizeof(cookie);
#endif

	zone_init(&(zone_table->zone_bootstrap), Z_ZONE_BOOTSTRAP_NAME, zone_object_size, 0);
#ifdef USEZMALLOC
	zmalloc_init();
#endif
}

void zone_table_deinit()
{
	int i;
	size_t page_size = 0;
	zone_t zonep;
    zone_t bootstrap_zonep = NULL;
	page_mapped_t page_p;
	page_mapped_t unmap_page;
	int ret;

	if(!zone_table)
		return;
	
	if(!zone_table->num_zone)
		goto clear_zone_table;
	
	// destroy all zones in table_table
	for(i = 0; i < zone_table->capacity; i++){
		if(!zone_table->zones[i])
			continue;
		// destroy a hole tree
		ZONE_BLTREE_DESTROY(zone_table->zones[i]);
	}

	// destroy zone_bootstrap
	zone_destroy(&(zone_table->zone_bootstrap));

clear_zone_table:
	page_size = round_up(sizeof(struct zone_hashtable) + DEFAULT_ZONE_SIZE * sizeof(struct zone), MAX_PAGE_SIZE);
	ret = munmap(zone_table, page_size);
	if(ret < 0){
		fprintf(stderr, "Unable to mumap zone_table\n");
		abort();
	}

	zone_table = NULL;
}

void zone_init(zone_t zone, const char *zone_name, size_t object_size, uint8_t is_mapped)
{
	page_mapped_t new_page;

	if(zone_name)
		strncpy(zone->zone_name, zone_name, sizeof(zone->zone_name) - 1);

	if(object_size > MAX_PAGE_SIZE * 4){
		fprintf(stderr, "Object is too large\n");
		abort();
	}

	zone->object_size = object_size;

	if(is_mapped){
		// map first page for this zone
		new_page = map_new_page(object_size);
		if(!new_page){
			fprintf(stderr,"Unable to map page_mapped_head for zone %s\n", zone->zone_name);
			abort();
		}

		zone->capacity = new_page->mapped_capacity;
		zone->num_page_mapped = 1;
		PAGEMAP_INIT_HEAD(zone, new_page);
	}
	
	zone->num_allocation = 0;
	zone->num_freed = 0;
	zone->page_min_num_free = NULL;
	zone->page_min_num_alloc = NULL;
}

void zone_create_internal(const char *zone_name, size_t object_size, uint8_t is_mapped)
{
	zone_t zone, d_zone = NULL;
	uint32_t idx = 0;
	size_t page_size;

	assert(zone_name != NULL);
	
	if(zone_table->num_zone >= DEFAULT_ZONE_SIZE){
		fprintf(stderr, "Unable to make a new zone for your zone %s\n", zone_name);
		abort();
	}

	idx  = hash_string(zone_name) % zone_table->capacity;
	zone = zone_table->zones[idx];
	
	// allocating a new temporary zone
	d_zone = (zone_t)zone_alloc_internal(Z_ZONE_BOOTSTRAP_NAME);
	if(!d_zone){
		fprintf(stderr, "Unable to create zone %s\n", zone_name);
		abort();
	}
	
	bzero((void *)d_zone, sizeof(struct zone));
	strncpy(d_zone->zone_name, zone_name, sizeof(zone->zone_name) - 1);
	d_zone->flags |= Z_ZONE_BOOTSTRAP;

	if(zone) {
		// zone duplicate , insert d_zone into balance tree
		zone_table->zones[idx] = ZONE_BLTREE_INSERT(zone, d_zone);
		zone = d_zone;
	} else {
		// store this zone into zone_table
		zone_table->zones[idx] = d_zone;
		zone = d_zone;
		zone_table->num_zone++;
	}

    // initialize attributes for this new zone
#ifdef USECOOKIE
	// use secure cookie
	object_size += sizeof(cookie);
#endif

	zone_init(zone, NULL, object_size, is_mapped);
}


void zone_create(const char *zone_name, size_t object_size)
{
	assert(zone_name != NULL);
	if(strncmp(zone_name, Z_ZONE_BOOTSTRAP_NAME, sizeof(Z_ZONE_BOOTSTRAP_NAME)) == 0){
		fprintf(stderr, "Invalid zone name\n");
		abort();
	}

	zone_create_internal(zone_name, object_size, 0);
}

void zone_destroy(zone_t zonep)
{
	page_mapped_t page_p, unmap_page;
	uint32_t zone_flags;

	assert(zonep != NULL);

	if(PAGEMAP_HEAD(zonep)){
		page_p = PAGEMAP_TAIL(zonep);//zonep->page_mapped_head->prev;
		// unmap all mapped-page in this zone
		do{
			unmap_page = page_p;
			page_p = page_p->prev;
			if(page_unmap_page(unmap_page, zonep->object_size) < 0){
				fprintf(stderr, "Unable to mumap base_address of zone %s\n", zonep->zone_name);
				abort();
			}
		}while(page_p != PAGEMAP_HEAD(zonep));
	}

	zone_flags = zonep->flags;
	bzero((void *)zonep, sizeof(struct zone));

	if(zone_flags & Z_ZONE_BOOTSTRAP){
		// free a zone was created in zone_bootstrap
		zone_free_internal(Z_ZONE_BOOTSTRAP_NAME, zonep);
	}
}

void *zone_alloc(const char *zone_name)
{
	if(strncmp(zone_name, Z_ZONE_BOOTSTRAP_NAME, sizeof(Z_ZONE_BOOTSTRAP_NAME)) == 0){
		fprintf(stderr, "Invalid zone name\n");
		abort();
	}

	return zone_alloc_internal(zone_name);
}

void *zone_alloc_internal(const char *zone_name)
{
	zone_t zone = NULL;
	void * ret_ptr = NULL;
	page_mapped_t pagep;
	size_t chunk_idx;
	size_t num_free_max;
	uint32_t idx, bit_idx;

	zone = zone_table_get_zone(zone_name);
	if(!zone){
		fprintf(stderr, "Invalid zone %s\n", zone_name);
		abort();
	}

	if(!zone->num_freed) {
		// we don't have any freed chunk to reuse
		if(zone->page_min_num_alloc && \
				zone->page_min_num_alloc->mapped_num_allocation + 1 < zone->page_min_num_alloc->mapped_capacity){
			// hack way to get new chunk
			pagep = zone->page_min_num_alloc;
#ifdef USECOOKIE
			if(memcmp(PAGEMAP_COOKIE_PTR(pagep), (void *)&cookie, sizeof(cookie)) != 0){
				fprintf(stderr, "Corrupted `pagep` of zone %s\n", zone->zone_name);
				abort();
			}
#endif

			if(pagep->mapped_num_allocation + 1 < pagep->mapped_capacity){
return_new_pointer:
				ret_ptr = pagep->cur_address;
				pagep->cur_address = (void *)((size_t)pagep->cur_address + zone->object_size);
#ifdef USECOOKIE
				memcpy(CHUNK_COOKIE_PTR(ret_ptr, zone->object_size - sizeof(cookie)), \
													(void *)&cookie, sizeof(cookie));
#endif
				pagep->mapped_num_allocation++;
				zone->num_allocation++;
				return ret_ptr;
			}
		}

		// unable to find any free space to alloc, map new page
		pagep = map_new_page(zone->object_size);
		if(!pagep){
			fprintf(stderr, "Unable to map address to pagep->base_address for zone %s\n", zone->zone_name);
			abort();
		}
		zone->num_page_mapped++;
		zone->capacity += pagep->mapped_capacity;
		
		if(zone->page_mapped_head){
			// append to zone->page_mapped_head doubly linkedlist
			PAGEMAP_APPEND(zone, pagep);
		} else {
			// init first mapped for this zone
			PAGEMAP_INIT_HEAD(zone, pagep);
		}

		zone->page_min_num_alloc = pagep; // best page to mark min_num_alloc
		goto return_new_pointer;
	}

	/* Use freed chunks */

	assert(zone->num_freed != 0);
	
	if(!zone->page_min_num_free || zone->page_min_num_free->mapped_num_free){
		// search for freed chunk
		pagep = PAGEMAP_HEAD(zone);
		zone->page_min_num_free = NULL;
		num_free_max = 0xFFFFFFFF;
		// find page has smallest mapped_num_free
		do{
			if(!pagep->mapped_num_free){
				pagep = pagep->next;
				continue;
			}

			if(pagep->mapped_num_free < num_free_max){
				zone->page_min_num_free = pagep;
				num_free_max = pagep->mapped_num_free;
			}
				
			pagep = pagep->next;
		}while(pagep != PAGEMAP_HEAD(zone));

		assert(zone->page_min_num_free != NULL);
		
	}

	pagep = zone->page_min_num_free;
	chunk_idx = bitmap_find_idx(pagep->bitmap, pagep->mapped_capacity);
	if((int64_t)chunk_idx < 0){
		// corrupted bitmap
		fprintf(stderr, "Unable to find any free chunk in zone %s\n", zone->zone_name);
		abort();
	}

	idx = chunk_idx / BIT_ARRAY_SIZE;
	bit_idx = chunk_idx % BIT_ARRAY_SIZE;
	// checking bit for this chunk to avoid double free chunk
	if(BIT64_IS_NOT_SET(pagep->bitmap[idx], bit_idx)){
		// corrupted bitmap
		fprintf(stderr, "Corrupted bitmap of zone %s\n", zone->zone_name);
		abort();
	}

	BIT64_CLEAR(pagep->bitmap[idx], bit_idx);// mark this chunk was allocated
	ret_ptr = (void *)((uint8_t *)pagep->base_address + chunk_idx * zone->object_size);

	pagep->mapped_num_allocation++;
	pagep->mapped_num_free--;

	zone->num_allocation++;
	zone->num_freed--;

	if(zone->page_min_num_free->mapped_num_free == 0){
		zone->page_min_num_free = NULL;
	}
	
	return ret_ptr; 
}

void zone_free(const char *zone_name, void *ptr)
{
	if(strncmp(zone_name, Z_ZONE_BOOTSTRAP_NAME, sizeof(Z_ZONE_BOOTSTRAP_NAME)) == 0){
		fprintf(stderr, "Invalid zone name\n");
		abort();
	}

	return zone_free_internal(zone_name, ptr);
}

void zone_free_internal(const char *zone_name, void *ptr)
{
	zone_t zone = NULL;
	size_t chunk_idx = 0;
	size_t end_address, base_address;
	uint32_t idx, bit_idx;
	page_mapped_t pagep;
	page_mapped_t pagep_min_num_free;
	uint8_t is_valid = 0;

	zone = zone_table_get_zone(zone_name);
	if(!zone){
		fprintf(stderr, "Invalid zone %s\n", zone_name);
		abort();
	}
	
	// make sure `ptr` is inside our mapped page
	pagep = PAGEMAP_HEAD(zone);
	do {
#ifdef USECOOKIE
		if(memcmp(PAGEMAP_COOKIE_PTR(pagep), (void *)&cookie, sizeof(cookie)) != 0){
			fprintf(stderr, "Corrupted `pagep` of zone %s\n", zone->zone_name);
			abort();
		}
#endif
		end_address = round_up((size_t)pagep->base_address + pagep->mapped_capacity * zone->object_size, MAX_PAGE_SIZE);
		base_address = (size_t)pagep->base_address;
		if(base_address <= (size_t)ptr && (size_t)ptr < end_address){
			is_valid = 1;
			break;
		}

		pagep = pagep->next;
	} while(pagep != PAGEMAP_HEAD(zone));

	if(!is_valid){
		fprintf(stderr, "Invalid pointer: %p\n", ptr);
		abort();
	}

	if (((size_t)ptr - (size_t)base_address) % zone->object_size){
		fprintf(stderr, "Invalid pointer: %p\n", ptr);
		abort();
	}

#ifdef USECOOKIE
	if(memcmp(CHUNK_COOKIE_PTR(ptr, zone->object_size - sizeof(cookie)), \
											(void *)&cookie, sizeof(cookie)) != 0){
		fprintf(stderr, "Corrupted chunk: %p\n", ptr);
		abort();
	}
#endif

	chunk_idx = ((size_t)ptr - (size_t)base_address) / zone->object_size;
	idx = chunk_idx / BIT_ARRAY_SIZE;
	bit_idx = chunk_idx % BIT_ARRAY_SIZE;
	// make sure this chunk isn't freed before
	if (BIT64_IS_SET(pagep->bitmap[idx], bit_idx)){
		fprintf(stderr, "Zone: %s  - Double free corrution!!", zone->zone_name);
		abort();
	}
	BIT64_SET(pagep->bitmap[idx], bit_idx); // mark this chunk was freed

	pagep->mapped_num_allocation--;
	pagep->mapped_num_free++;
	zone->num_allocation--;
	zone->num_freed++;

	if(!pagep->mapped_num_free){
		// search for other pagep_min_num_free
		zone->page_min_num_free = PAGEMAP_HEAD(zone)->next;
		for(pagep = PAGEMAP_HEAD(zone)->next; pagep->next != PAGEMAP_HEAD(zone); pagep = pagep->next){
			if(pagep->mapped_num_free < pagep_min_num_free->mapped_num_free){
				pagep_min_num_free = pagep;
			}
		}
		// update for this field to speed up zone_alloc and zone_free
		zone->page_min_num_free = pagep_min_num_free;
	}

	if(pagep->mapped_num_free >= pagep->mapped_capacity - 1 && zone->num_page_mapped >= PAGE_MAPPED_MAX_THRESHOLD){
		// unmap this page if all elements in this page was freed
		zone->capacity -= pagep->mapped_capacity;
		zone->num_freed -= pagep->mapped_num_free;
		zone->num_page_mapped--;

		PAGEMAP_REMOVE(zone, pagep);

		if(pagep == zone->page_min_num_free)
			zone->page_min_num_free = NULL;

		if(pagep == zone->page_min_num_alloc)
			zone->page_min_num_alloc = NULL;

		assert(page_unmap_page(pagep, zone->object_size) >= 0);

		if(!zone->page_min_num_alloc){
			// search for new ptr page_min_num_alloc
			pagep = PAGEMAP_HEAD(zone);
			do{
				if(pagep->mapped_num_allocation < pagep->mapped_capacity){
					zone->page_min_num_alloc = pagep;
				}
				pagep = pagep->next;
			}while(pagep->next != PAGEMAP_HEAD(zone));
		}
	}
}

#ifdef USEZMALLOC
void* zmalloc(uint64_t size)
{
	uint64_t malloc_size;
	uint32_t chunk_idx;
	const char *zmalloc_chunk_name;

	malloc_size = round_up(size, MIN_CHUNK_SIZE);
	chunk_idx = (malloc_size / MIN_CHUNK_SIZE) - 1;

	if(chunk_idx > MAX_MALLOC_SIZE_NAME){
		fprintf(stderr, "Invalid zmalloc size, size must be less or equal 8192\n");
		return NULL;
	}

	zmalloc_chunk_name = z_malloc_zone_name[chunk_idx];
	return zone_alloc_internal(zmalloc_chunk_name);
}

void zfree(void *ptr, uint64_t ptr_size)
{
	uint32_t chunk_idx;
	const char *zmalloc_chunk_name;

	ptr_size = round_up(ptr_size, MIN_CHUNK_SIZE);
	chunk_idx = (ptr_size / MIN_CHUNK_SIZE) - 1;

	if(chunk_idx > MAX_MALLOC_SIZE_NAME){
		fprintf(stderr, "Invalid zfree size, size must be less or equal 8192\n");
		return;
	}

	zmalloc_chunk_name = z_malloc_zone_name[chunk_idx];
	zone_free_internal(zmalloc_chunk_name, ptr);
}

char* zstrdup(const char *str)
{
	uint32_t s_length = strlen(str);
	char *new_s;

	new_s = zmalloc(s_length + 1);
	if(!new_s)
		return NULL;
	
	strncpy(new_s, str, s_length);
	new_s[s_length] = '\x00';
	return new_s;
}

void zstrfree(char *str)
{
	zfree(str, strlen(str) + 1);
}

#endif

#ifdef DEBUG
void zone_list()
{
	int i, k;
	zone_t zone;
	page_mapped_t pagep;

	for(i = 0; i < zone_table->capacity; i++){
		if(!zone_table->zones[i]) continue;
		zone = zone_table->zones[i];

		printf("Zone: %s\n", zone->zone_name);
		printf("object_size: %ld\n", zone->object_size);
		printf("capacity: %ld\n", zone->capacity);
		printf("num_allocation: %ld\n", zone->num_allocation);
		printf("num_freed: %ld\n", zone->num_freed);
		printf("num_page_mapped: %ld\n", zone->num_page_mapped);
		printf("page_mapped:\n");

		pagep = PAGEMAP_HEAD(zone);
		do {
			printf("-----------------------------------------------\n");
			printf("\tcapacity: %ld\n",       pagep->mapped_capacity);
			printf("\tbase_address: %p\n",    pagep->base_address);
			printf("\tnum_allocation: %ld\n", pagep->mapped_num_allocation);
			printf("\tnum_free: %ld\n",       pagep->mapped_num_free);
			printf("\tbitmap: ");
			for(k = 0; k < round_up(pagep->mapped_capacity, BIT_ARRAY_SIZE) / BIT_ARRAY_SIZE; k++){
				printf("%lld ", pagep->bitmap[k]);
			}
			printf("\n");
			pagep = pagep->next;
		} while(pagep != PAGEMAP_HEAD(zone));
	}
}
#endif
