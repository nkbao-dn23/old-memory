/*
 * Author: peter
 * Note structures defination
 */

#include <stddef.h>
#include <stdint.h>
#include "libzone.h"

#ifndef NOTE_H
#define NOTE_H

#define BUFFER_SIZE 256
#define NOTE_ZONE_NAME "note"
#define NOTE_ARRAY_ZONE_NAME "note_array"

struct reference;
typedef struct reference* reference_t;

struct reference {
	uint32_t ref_count;
	void (*dealloc_func)(reference_t);
};

struct Note {
	char n_name[BUFFER_SIZE];
	uint64_t n_word_count;
	char *n_buffer;
	struct reference n_ref;
};

typedef struct Note* Note_t;

struct NoteArray {
	Note_t *note_array;
	uint32_t note_size;
	uint32_t note_count;
};

typedef struct NoteArray* NoteArray_t;

#define NOTE_ALLOC zone_alloc(NOTE_ZONE_NAME)
#define NOTE_FREE(note_ptr) zone_free(NOTE_ZONE_NAME, note_ptr)

#define NOTE_ARRAY_ALLOC zone_alloc(NOTE_ARRAY_ZONE_NAME)
#define NOTE_ARRAY_FREE(note_array_ptr) zone_free(NOTE_ARRAY_ZONE_NAME, note_array_ptr)

#define CAST_TO_REF(note_ptr) ((reference_t)((void *)note_ptr + offsetof(struct Note, n_ref)))
#define CAST_TO_NOTE(ref_ptr) ((Note_t)((void *)ref_ptr - offsetof(struct Note, n_ref)))

void reference_init(reference_t ref, void (*func_ptr)(reference_t));

void Note_Ref(reference_t ref);
void Note_Rele(reference_t ref);

#define NOTE_REF(note_ptr) \
	do{ \
		if(note_ptr) { \
			Note_Ref(CAST_TO_REF(note_ptr)); \
		} \
	}while(0)

#define NOTE_RELE(note_ptr) \
	do{ \
		if(note_ptr) { \
			Note_Rele(CAST_TO_REF(note_ptr)); \
		} \
	}while(0)

#define NOTE_IS_REFERENCED(note_ptr) (CAST_TO_REF(note_ptr)->ref_count > 1)

#define NOTE_NAME(note_p)         (note_p->n_name)
#define NOTE_WORD_COUNT(note_p)   (note_p->n_word_count)
#define NOTE_CONTENT(note_p)      (note_p->n_buffer)

#define NOTEARRAY_CUR_SIZE(note_array_ptr) (note_array_ptr->note_count)
#define NOTEARRAY_CAPACITY(note_array_ptr) (note_array_ptr->note_size)
#define NOTEARRAY_ARRAY(note_array_ptr)    (note_array_ptr->note_array)

void Note_Init(Note_t anote, const char *name, uint64_t word_count, char *note_buffer);
void Note_Dealloc(reference_t anote_ref);

NoteArray_t NoteArray_Create(NoteArray_t a_note_array, uint32_t capacity);
void NoteArray_Append(NoteArray_t a_array, Note_t a_note);
void NoteArray_Insert(NoteArray_t a_array, uint32_t idx, Note_t a_note);
void NoteArray_Remove(NoteArray_t a_array, uint32_t idx);
Note_t NoteArray_Get(NoteArray_t a_array, uint32_t idx);
void NoteArray_Destroy(NoteArray_t a_note_array);

#endif
