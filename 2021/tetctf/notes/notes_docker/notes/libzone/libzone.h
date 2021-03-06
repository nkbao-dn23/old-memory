/*
	Simple Zone Allocator
	Author: peter
*/
#ifndef LIBZONE_H
#define LIBZONE_H

#include <stdint.h>
#include <sys/cdefs.h>
// use Balance Tree to speed up search time for duplicate hash entry
#include "bltree.h"

#define PAGE_MAPPED_MAX_THRESHOLD 3
#define MAX_PAGE_SIZE 4096

#ifdef USE_ZONE_SIZE
#define DEFAULT_ZONE_SIZE USE_ZONE_SIZE
#else
#define DEFAULT_ZONE_SIZE 256
#endif

#define PAGE_MAP_MAX_BITMAP 512
// #define MAX_INLINE_BITMAP 128
#define MAX_NAME 64
#define BIT_PER_BYTE sizeof(uint64_t)
#define BIT_ARRAY_SIZE (8 * BIT_PER_BYTE)
#define MAX_OBJECT_PER_MAP 16
#define Z_ZONE_BOOTSTRAP_NAME "zone_bootstrap"
#define Z_ZONE_BOOTSTRAP 1

#define OUTOFMEM -2
#define MAPERR -1

struct page_mapped;
typedef struct page_mapped* page_mapped_t;

struct page_mapped {
	size_t mapped_capacity;
	size_t mapped_num_allocation;
	size_t mapped_num_free;
	void *base_address;
	void *cur_address;
	page_mapped_t next;
	page_mapped_t prev;
	uint64_t bitmap[];
};

struct zone {
	char zone_name[MAX_NAME];
	uint32_t flags;
	size_t object_size;
	size_t capacity;
	size_t num_allocation;
	size_t num_freed;
	size_t num_page_mapped;
	page_mapped_t page_mapped_head;
	page_mapped_t page_min_num_free;
	page_mapped_t page_min_num_alloc;
	// because hashtable could have duplicate item
	// I add this Balance Tree for each node in hashtable to store duplicate item
	// to make sure when we search a zone by name the time complexity is O(log(N))
	BLTREE_ROOT_DECL(blnode);
};
typedef struct zone* zone_t;

struct zone_hashtable {
	size_t capacity;
	size_t num_zone;
	// create a fixed zone to allocate struct zone
	struct zone zone_bootstrap;
	zone_t zones[]; // zone_array pointer
};
typedef struct zone_hashtable* zone_hastable_t; 

extern zone_hastable_t zone_table;
extern uint64_t        cookie[2]; // 0x10 bytes for cookie padding

// #define PAGE_NEXT_CHUNK(pagep, object_size) (void *)((uint8_t *)pagep->cur_address + object_size * )
#define PAGEMAP_INIT_HEAD(zone, pagep) do {\
		zone->page_mapped_head       = pagep;\
		zone->page_mapped_head->next = zone->page_mapped_head;\
		zone->page_mapped_head->prev = zone->page_mapped_head;\
	} while(0)

#define PAGEMAP_HEAD(zone) zone->page_mapped_head
#define PAGEMAP_TAIL(zone) zone->page_mapped_head->prev

#define PAGEMAP_APPEND(zone, pagep) do { \
		page_mapped_t tailp; \
		tailp = PAGEMAP_TAIL(zone); \
		tailp->next = pagep; \
		pagep->prev = tailp; \
		pagep->next = PAGEMAP_HEAD(zone); \
		PAGEMAP_TAIL(zone) = pagep; \
	}while(0)

#define PAGEMAP_REMOVE(zone, pagep) do { \
		page_mapped_t ppage; \
		if(PAGEMAP_HEAD(zone) == pagep) {\
			ppage = PAGEMAP_HEAD(zone)->next; \
			ppage->prev = PAGEMAP_TAIL(zone); \
			PAGEMAP_TAIL(zone)->next = ppage; \
			PAGEMAP_HEAD(zone) = ppage; \
		} else if(PAGEMAP_TAIL(zone) == pagep) { \
			ppage = PAGEMAP_TAIL(zone)->prev; \
			ppage->next = PAGEMAP_HEAD(zone); \
			PAGEMAP_TAIL(zone) = ppage; \
		} else {\
			for(ppage = PAGEMAP_HEAD(zone); ppage->next != pagep; ppage = ppage->next); \
			ppage->next = pagep->next; \
			pagep->next->prev = ppage; \
		}\
	}while(0)

#define BIT64_SET(bit_array, bit_idx) (bit_array |= (1ULL << bit_idx))
#define BIT64_CLEAR(bit_array, bit_idx) (bit_array &= ~(1ULL << bit_idx))
#define BIT64_IS_SET(bit_array, bit_idx) ((bit_array >> bit_idx) & 1)
#define BIT64_IS_NOT_SET(bit_array, bit_idx) (!BIT64_IS_SET(bit_array, bit_idx))

__BEGIN_DECLS

void  zone_create(const char *zone_name, size_t object_size); // create a new zone for specific object
void* zone_alloc(const char *zone_name); // alloc a new object 
void  zone_free(const char *zone_name, void *ptr); // free an object

#ifdef DEBUG
void  zone_list();
#endif

#ifdef USEZMALLOC
#define MIN_CHUNK_SIZE 0x10
void* zmalloc(uint64_t size);
void  zfree(void *ptr, uint64_t ptr_size);
char* zstrdup(const char *str);
void  zstrfree(char *str);
#endif

__END_DECLS

// don't public this functions
// void zone_table_init();
// void zone_table_deinit();
#endif
