/*
 * Author: peter
 * Note's implementations
 */

#include "note.h"
#include <stdlib.h>
#include <string.h>
#include <assert.h>

void reference_init(reference_t ref, void (*func_ptr)(reference_t))
{
	assert(ref != NULL);
	ref->ref_count = 1;
	ref->dealloc_func = func_ptr;
}

void Note_Init(Note_t a_note, const char *name, uint64_t note_word_count, char *note_buffer)
{
	assert(a_note != NULL);
	
	bzero((void *)&(a_note->n_name), sizeof(a_note->n_name));
	memcpy(a_note->n_name, name, sizeof(a_note->n_name) - 1);
	
	if(note_buffer){
		a_note->n_word_count = note_word_count;
		a_note->n_buffer = note_buffer;
	}

	reference_init(CAST_TO_REF(a_note), Note_Dealloc);
}

void Note_Dealloc(reference_t ref)
{
	Note_t noteptr;
	assert(ref != NULL);

	noteptr = CAST_TO_NOTE(ref);
	if(noteptr->n_buffer){
		free(noteptr->n_buffer);
	}

	NOTE_FREE(noteptr);
}

void Note_Ref(reference_t a_ref)
{
	if(!a_ref)
		return;

	a_ref->ref_count++;
}

void Note_Rele(reference_t a_ref)
{
	if(!a_ref)
		return;

	--a_ref->ref_count;
	if(a_ref->ref_count == 0){
		a_ref->dealloc_func(a_ref);
	}
}

NoteArray_t NoteArray_Create(NoteArray_t a_array, uint32_t capacity)
{
	if(!a_array){
		// allocate a note_array
		a_array = NOTE_ARRAY_ALLOC;
		a_array->note_size = capacity;
		a_array->note_count = 0;
		a_array->note_array = (Note_t *)malloc(capacity * sizeof(Note_t));
		
		bzero((void *)a_array->note_array, sizeof(capacity * sizeof(Note_t)));
		goto return_array;
	}

	if(a_array->note_size <= capacity)
		goto return_array;
	
	// extend the note_array field
	a_array->note_size = capacity;
	a_array->note_array = (Note_t *)realloc(a_array->note_array, capacity * sizeof(Note_t));

return_array:
	return a_array;
}

void NoteArray_Append(NoteArray_t a_array, Note_t a_note)
{
	if(!a_array)
		return;

	if(a_array->note_count + 1 < a_array->note_size){
		NOTE_REF(a_note);
		a_array->note_array[a_array->note_count++] = a_note;
	}
}

void NoteArray_Insert(NoteArray_t a_array, uint32_t idx, Note_t a_note)
{
	uint32_t i;

	if(!a_array)
		return;

	if(a_array->note_count + 1 >= a_array->note_size){
		// extend a_array
		NoteArray_Create(a_array, a_array->note_size * 2);
	}

	if(idx < a_array->note_size && a_array->note_count + 1 < a_array->note_size){
		if(idx >= a_array->note_count){
			NoteArray_Append(a_array, a_note);
			return;
		}

		for(i = idx; i < a_array->note_count; i++){
			a_array->note_array[i + 1] = a_array->note_array[i];
		}

		NOTE_REF(a_note);
		a_array->note_array[idx] = a_note;
		a_array->note_count++;
	}
}

void NoteArray_Remove(NoteArray_t a_array, uint32_t idx)
{
	uint32_t i;

	if(!a_array)
		return;
	
	if(idx >= a_array->note_count)
		return;

	NOTE_RELE(a_array->note_array[idx]);
	
	if(idx + 1 == a_array->note_count){
		a_array->note_array[idx] = NULL;
		goto remove_end;
	}
	
	for(i = idx; i < a_array->note_count; i++){
		a_array->note_array[i] = a_array->note_array[i + 1];
	}
remove_end:
	--a_array->note_count;
}

Note_t NoteArray_Get(NoteArray_t a_array, uint32_t idx)
{
	if(!a_array)
		return NULL;
	
	if(idx >= a_array->note_count)
		return NULL;

	NOTE_REF(a_array->note_array[idx]);
	return a_array->note_array[idx];
}

void NoteArray_Destroy(NoteArray_t a_array)
{
	int i;

	if(a_array->note_array){
		for(i = 0; i < a_array->note_count; i++){
			NOTE_RELE(a_array->note_array[i]);
		}

		free(a_array->note_array);
	}

	NOTE_ARRAY_FREE(a_array);
}
