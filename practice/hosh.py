# a unix shell by Hobson
# based on a C program in Advanced Programming in the UNIX(R) Environment, Third Edition
# section 1.6

import sys  # argv, stdin, stdout, stderr
import os   # fork


def main(argv):
    print("%% ")
    buf = sys.stdin.readline()
    while (buf and buf is not '\n'):
        pid = 0
        try:
            pid = os.fork()
        except:
            print('fork error')
        if pid == 0:  # child
            bufs = buf.split(' ')
            try:
                retval = os.execlp(*bufs)
                print retval
                return 127
            except:
                sys.stderr.write("couldn't execute: %s" % buf)
                return 0
        elif pid:
            status = os.waitpid(pid)
            if status < 0:
                sys.stderr.write("waitpid error")
        print("%% ")
        buf = sys.stdin.readline()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
