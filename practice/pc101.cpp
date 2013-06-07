// programming challenge 110101
// http://www.programming-challenges.com/pg.php?page=studenthome
// 3n + 1 problem


#include <sys/types.h>      /* some systems still require this */
// #include <sys/stat.h>
// #include <sys/termios.h>    /* for winsize */

// #if defined(MACOS) || !defined(TIOCGWINSZ)
// #include <sys/ioctl.h>
// #endif

#include <stdio.h>      
#include <stdlib.h>
#include <stddef.h>     /* for offsetof */
#include <string.h>
// #include <unistd.h>
// #include <signal.h>     /* for SIG_ERR */

int main(void) {
    char    buf[4096];   
    pid_t   pid;
    int     status;
    int     k;

    printf("%% ");  /* print prompt (printf requires %% to print %) */
    while (fgets(buf, MAXLINE, stdin) != NULL) {
        if (buf[strlen(buf) - 1] == '\n') {
            buf[strlen(buf) - 1] = 0; /* replace newline with null */
            sscanf(buf, "%d %d", &i, &j)
            k = i;
            while(j != i) {
            	if (!(i % 2)) {
            		k /= 2;
            	} else {
            		k *= 2;
            	}
            	printf("%d\n", k)
            }
        }
    }

