#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define MAX_INDEX 8
char * HEAP_PTRS[MAX_INDEX];
int SIZES[MAX_INDEX];
int INDEX = 0;

static void new_dream() {
	int length = 0;
	puts("How long is your dream?");
	scanf("%d", &length);
	char * dream_ptr = malloc(length);
	puts("What are the contents of this dream?");
	read(0, dream_ptr, length);
	HEAP_PTRS[INDEX] = dream_ptr;
	SIZES[INDEX] = length;
	INDEX = INDEX + 1;
	return;
}

static void read_dream() {
	puts("Which dream would you like to read?");
	int index = 0;
	scanf("%d", &index);
	if (index > INDEX){
		puts("Maybe you need to sleep...");
		return;
	}
	char * this_dream = HEAP_PTRS[index];
	printf("%s", this_dream);
	return;
}

static void edit_dream() {
	puts("Which dream would you like to change?");
	int index = 0;
	scanf("%d", &index);
	if (index > INDEX) {
		puts("You can't change future");
		return;
	}
	char * this_dream = HEAP_PTRS[index];
	int length = SIZES[index];
	read(0, this_dream, length);
	this_dream[length] = '\0';
	return;
}

static void delete_dream(){
	puts("Which dream would you like to delete?");
	int index = 0;
	scanf("%d", &index);
	if (index > INDEX) {
		puts("Oops, No dream here");
		return;
	}
	char * this_dream = HEAP_PTRS[index];
	free(this_dream);
	HEAP_PTRS[index] = 0;
	return;
}

int main() {
    int option = 0;
    setbuf(stdout, NULL);
    puts("Martin Luther King said: I have a dream!!!!\n");
    while (1) {
        printf("Do you have a dream?\n");
        printf("1: Write dream\n");
        printf("2: Read dream\n");
        printf("3: Edit dream\n");
        printf("4: Delete dream\n");
		printf("5: Quit\n> ");
        scanf("%d", &option);
        switch(option) {
            case 1:
                new_dream();
                break;
            case 2:
                read_dream();
                break;
            case 3:
                edit_dream();
                break;
            case 4:
                delete_dream();
                break;
			case 5:
				exit(0);
            default:
                puts("What are you doing?!\n");
                break;
        }
	}
    return 0;
}
