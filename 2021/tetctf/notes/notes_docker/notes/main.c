/*
 * Author: peter
 * Main implementation of Note
 */
#include "note.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <assert.h>

#define NOTEARRAY_DEFAULT_CAPACITY 128
NoteArray_t gNoteArray;

#define KEY_SIZE_VALIDATE(key_size) if(key_size > DEFAULT_KEY_SIZE) key_size = DEFAULT_KEY_SIZE;
#define NOTE_WORD_COUNT_VALIDATE(word_count) if(word_count > 0x1000) word_count = 0x1000;

void init_required_zones()
{
	zone_create(NOTE_ZONE_NAME, sizeof(struct Note));
	zone_create(NOTE_ARRAY_ZONE_NAME, sizeof(struct NoteArray));
}

void read_str(char *buf, uint32_t size)
{
	int i = 0;
	char chr;

	while(i < size){
		chr = (char)fgetc(stdin);
		if(chr == '\n'){
			buf[i] = '\x00';
			break;
		}
		buf[i++] = chr;
	}
}

uint32_t read_int()
{
	char buf[16] = {0};

	read_str(buf, sizeof(buf) - 1);
	return strtoul(buf, NULL, 10);
}

void xor(char *buffer, uint64_t size, char *key, uint64_t key_size)
{
	int i;

	if(key_size == 0)
		return;

	for(i = 0; i < size; i++){
		buffer[i] ^= key[i % key_size];
	}
}

int main()
{
	uint32_t op, idx, i;
	uint32_t word_count;
	char *buff;
	char local_buf[512];
	Note_t a_note = NULL;
	Note_t t_note = NULL;
	char is_run = 1;
	uint32_t key_size = 0;
	uint32_t note_name_len = 0;

	init_required_zones();
	
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);

	gNoteArray = NULL;
	gNoteArray = NoteArray_Create(NULL, NOTEARRAY_DEFAULT_CAPACITY);
	assert(gNoteArray != NULL);

	while(is_run){
		puts("======== Note Manager ========");
		puts("1. Create Note");
		puts("2. Edit Note");
		puts("3. Save Note");
		puts("4. Copy Note");
		puts("5. List Note");
		puts("6. Remove Note");
		puts("7. Exit");
		printf("$ ");
		op = read_int();
		switch(op) {
			case 1:
				if(a_note)
					NOTE_RELE(a_note);
				
				a_note = NOTE_ALLOC;
				printf("Note Name: ");
				bzero(local_buf, sizeof(local_buf));
				read_str(local_buf, sizeof(a_note->n_name) - 1);
				printf("How many words do you want? ");
				word_count = read_int();
				NOTE_WORD_COUNT_VALIDATE(word_count)

				buff = NULL;
				if(word_count){
					buff = (char *)malloc(word_count);
					bzero(buff, word_count);
					puts("Enter your content:");
					fread(buff, 1, word_count, stdin);
				}

				Note_Init(a_note, (const char *)local_buf, word_count, buff);
				puts("Done.");
				break;

			case 2:
				printf("Which note do you want to edit?");
				idx = read_int();
				t_note = NoteArray_Get(gNoteArray, idx);
				if(!t_note){
					printf("Your requested note doesn't exists\n");
					break;
				}

				if(NOTE_IS_REFERENCED(t_note)){
					NOTE_RELE(t_note);
					a_note = NOTE_ALLOC;
					buff = (char *)malloc(NOTE_WORD_COUNT(t_note));
					memcpy(buff, NOTE_CONTENT(t_note), NOTE_WORD_COUNT(t_note));
					Note_Init(a_note, (const char *)&(t_note->n_name), NOTE_WORD_COUNT(t_note), buff);
					NoteArray_Insert(gNoteArray, idx, a_note);
					t_note = a_note;
				}

				printf("Note Name: ");
				bzero(local_buf, sizeof(local_buf) - 1);
				read_str(local_buf, sizeof(t_note->n_name) - 1);
				note_name_len = strlen(local_buf);
				memcpy(t_note->n_name, local_buf, note_name_len);
				t_note->n_name[note_name_len] = '\x00';

				printf("How many words do you want? ");
				word_count = read_int();
				NOTE_WORD_COUNT_VALIDATE(word_count);

				if(word_count > NOTE_WORD_COUNT(t_note)){
					NOTE_CONTENT(t_note) = (char *)realloc(NOTE_CONTENT(t_note), word_count);
					NOTE_WORD_COUNT(t_note) = word_count;
				}
				fread(NOTE_CONTENT(t_note), 1, word_count, stdin);
				NOTE_RELE(t_note);
				puts("Done.");
				break;

			case 3:
				if(!a_note){
					puts("You don't have note to save");
					break;
				}
				printf("Which idx do you want to save?");
				idx = read_int();
				NoteArray_Insert(gNoteArray, idx, a_note);
				puts("Done.");
				break;
			case 4:
				printf("Which note do you want to copy?");
				idx = read_int();
				t_note = NoteArray_Get(gNoteArray, idx);
				if(!t_note){
					printf("Your note at index %d does not exist\n", idx);
					break;
				}

				printf("Which idx do you wanna save?");
				idx = read_int();
				NoteArray_Insert(gNoteArray, idx, t_note);
				NOTE_RELE(t_note);
				puts("Done.");
				break;

			case 5:
				if(NOTEARRAY_CUR_SIZE(gNoteArray) == 0){
					printf("Note Database is empty\n");
					break;
				}

				printf("Notes: \n");
				for(i = 0; i < NOTEARRAY_CUR_SIZE(gNoteArray); i++){
					printf("%d. [%s] %lld\n", i, NOTEARRAY_ARRAY(gNoteArray)[i]->n_name, \
										NOTEARRAY_ARRAY(gNoteArray)[i]->n_word_count);
				}
				printf("Which note do you want to read?");
				idx = read_int();
				
				t_note = NoteArray_Get(gNoteArray, idx);
				if(!t_note){
					printf("Note at %d do not exist\n", idx);
					break;
				}
				printf("Note [%s]\n", t_note->n_name);
				puts("Content:");
				fwrite(NOTE_CONTENT(t_note), 1, NOTE_WORD_COUNT(t_note), stdout);
				printf("\n");

				NOTE_RELE(t_note);
				puts("Done.");
				break;

			case 6:
				printf("Which note do you want to remove?");
				idx = read_int();
				NoteArray_Remove(gNoteArray, idx);
				puts("Done.");
				break;

			case 7:
				is_run = 0;
				break;

			default:
				break;
		}
		t_note = NULL;
	}

	if(a_note)
		NOTE_RELE(a_note);

	NoteArray_Destroy(gNoteArray);
	return 0;
}

