cmake_minimum_required(VERSION 3.10)
project(notes C)

set(SOURCE
	note.c
	main.c
)

if(CMAKE_BUILD_TYPE STREQUAL "Debug")
	set(NOTE_C_CFLAGS ${CMAKE_C_CFLAGS} -g)
	set(CMAKE_C_CFLAGS ${CMAKE_C_CFLAGS} -g -DUSECOOKIE=1 -DUSE_ZONE_SIZE=16)
else()
	set(NOTE_C_CFLAGS ${CMAKE_C_CFLAGS})
	set(CMAKE_C_CFLAGS ${CMAKE_C_CFLAGS} -DUSECOOKIE=1 -DUSE_ZONE_SIZE=16)
endif()

add_subdirectory(libzone)
set(LINK_LIBS zone)

include_directories(${CMAKE_CURRENT_BINARY_DIR})
include_directories(libzone)

add_executable(note ${SOURCE})
target_include_directories(note PUBLIC "${PROJECT_DIR}")
target_compile_options(note PUBLIC ${NOTE_C_CFLAGS})
target_link_libraries(note ${LINK_LIBS})
