# a unix shell by Hobson
# based on a C program in Advanced Programming in the UNIX(R) Environment, Third Edition
# section 1.6

import sys  # argv, stdin, stdout, stderr
import os   # fork


def main(argv):
    sys.stdout.write("%% ")
    buf = sys.stdin.readline()
    while (buf and buf is not '\n'):
        pid = 0
        try:
            pid = os.fork()
        except:
            print('fork error')
        if pid == 0:  # child
            bufs = buf.split(' ')
            if len(bufs) < 2:
                bufs += ['']
            retval = os.execlp(*bufs)
            if retval >= 0:
                return 127
            sys.stderr.write("couldn't execute: %s" % buf)
            return 0
        elif pid:
            try:
                status = os.waitpid(pid, 0)
            except OSError as e:
                sys.stderr.write("I/O error({0}): {1}".format(e.errno, e.strerror))
                status = (pid, -1)
            if status and len(status) == 2 and status[1] < 0:
                sys.stderr.write("waitpid error")
        sys.stdout.write("%% ")
        buf = sys.stdin.readline()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
