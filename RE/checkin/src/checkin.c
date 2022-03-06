#include <stdio.h>

void debug_output(char * out, int len){
    printf("\t");
    for (int i = 0; i < len; i++) {
        printf("%02hhX ", out[i]);
    }
    printf("\n\n");
    return;
}

char target[] = "\x0B\x94\xBA\x4B\xAA\xA6\x65\x8C\x30\x93\xE0\xA2\xCB\x50\xEB\xD2";
char trans[] = {14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7};

int main(){
    puts("###");
    puts("### Welcome to the world of RE~");
    puts("###");
    puts("");
    puts("");
    puts("This program consumes a uuid format key over stdin. Your target is to figure out (by reverse engineering this program) what that key is.");
    puts("");
    char key[20];
    scanf("%08x-%04hx-%04hx-%04hx-%02hhx%02hhx%02hhx%02hhx%02hhx%02hhx", key, key+4, key+6, key+8, key+10, key+11, key+12, key+13, key+14, key+15);
    puts("[+]Initial input:");
    debug_output(key, 16);
    // This challenge is now mangling your input using the `xor` mangler with key `0xd0`
    // This mangled your input, resulting in:
    //         b6 bc b1 b7 da 
    puts("Now mangling your input using the `xor` mangler");
    for (int i = 0; i < 16; i++) {
        key[i] ^= 0x87;
    }
    puts("[+]This mangled resulting in:");
    debug_output(key, 16);

    puts("Now mangling your input using the `shuffle` mangler");

    char tmp_key[20];
    for (int i = 0; i < 17; i++) {
        tmp_key[i] = key[i];
    }
    for (int i = 0; i < 16; i++) {
        key[i] = tmp_key[trans[i]];
    }

    puts("The mangling is done! The resulting bytes will be used for the final comparison.");
    puts("[+]Final result of mangling input:");
    debug_output(key, 16);
    puts("[+]Expected result:");
    debug_output(target, 16);
    puts("Checking the received license key!");
    puts("");
    
    int check = 0;

    for (int i = 0; i < 16; i++){
        check |= key[i] ^ target[i];
    }
    // compare
    if (0 == check) {
        puts("Correct! The flag is flag{input}");
    }
    else {
        puts("Wrong! No flag for you!\n");
    }
    return 0;
}

// b72dcc6c-4c13-5567-d70b-14e2253d8c21