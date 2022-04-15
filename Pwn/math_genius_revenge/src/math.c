#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void sighandler(int signum)
{
   printf("check sth wrong, please call the computer's admin\n");
   system("/bin/sh");
}

void init(){
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    alarm(30);
    signal(SIGFPE, sighandler);
}


int main(){
    init();
        int i, a, b, ans, cal, cnt = 0;
        srand((unsigned)time( NULL ) );
        int date = 3939;
        for (i = 0; i < 20; i ++){
                printf("round%d\n", i);
                a = abs(rand() % date);
        b = abs(rand() % date);
                printf("numberA = :%d\n", a);
        printf("numberB = :%d\n", b);
                cal = abs(rand() % 3);
                if (cal == 0){
                        printf("please tell me answer a + b:");
                        scanf("%d", &ans);
                        if (ans == a + b){
                                printf("right\n");
                                cnt ++;
                        }
                        else{
                                printf("wrong\n");
                        }
                        printf("\n");
                }
                else if(cal == 1){
                        printf("please tell me answer a * b:");
                        scanf("%d", &ans);
                        if (ans == a * b){
                                printf("right\n");
                                cnt ++;
                        }
                        else{
                                printf("wrong\n");
                        }
                        printf("\n");
                }
                else if(cal == 2){
                        printf("please tell me answer a - b:");
                        scanf("%d", &ans);
                        if (ans == a - b){
                                printf("right\n");
                                cnt ++;
                        }
                        else{
                                printf("wrong\n");
                        }
                        printf("\n");
                }
        }
        if (cnt > 19)
                printf("now, you are good at +/-/*, let's try div,give me two number:\n");
        scanf("%d %d", &a, &b);
        if (b != 0){
            ans = a/b;
            printf("please tell me answer a / b:");
            scanf("%d", &ans);
            if (ans == a / b){
                printf("right,you are genius\n");
                cnt ++;
            }
            else{
                printf("wrong\n");
            }
            printf("\n");
        }
        return 0;
}