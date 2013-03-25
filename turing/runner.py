"""

"""

import sys
from blessings import Terminal

def create_terminal_runner(machine, step=False):
    def run():
        s = step
        t = Terminal()
        def format_char(pos, cur, char):
            if pos == cur:
                return t.bold_blue(char)
            else:
                return char
        for l, (cur_state, tapes) in enumerate(machine):
            sys.stdout.write(t.green(t.bold('[%s] ' % str(l+1))))
            with t.location(20):
                sys.stdout.write(t.cyan(t.bold('[State %s] ' % str(cur_state))))
            for i, tape in enumerate(tapes):
                with t.location(40):
                    sys.stdout.write('[Tape %s] ' % i)
                    c = ''.join(tape.format(format_char, 15, 15))
                    sys.stdout.write(c)
                    if i < len(tapes) - 1:
                        sys.stdout.write('\n')
                    sys.stdout.flush()
            if not s:
                sys.stdout.write('\n')
            if s:
                f = input()
                if f.strip() == 'q':
                    sys.exit(0)
                if f.strip() == 'r':
                    s = False
    return run

if __name__ == '__main__':
    from turing import machine
    m = machine.Machine(tapes=('0000000000000000000000000000-0000000000'),
                         functions=(
                             ((1,1),((0,0,'r'),)),
                             ((1,2),(('-',1,'r'),)),
                             ((2,2),((1,1,'r'),)),
                             ((2,3),((0,1,'l'),)),
                             ((3,3),((1,1,'l'),)),
                             ((3,2),((0,1,'r'),)),
                             ((2,4),((None,'_','l'),)),
                             ((4,4),((1,'_','l'),)),
                         ),
                         blank='_')

    m2 = machine.Machine(tapes=('00000+00', None),
                         functions=(
                             ((1,2),((0,'_','r'),(None,'x','l'))),
                             ((2,2),((0,0,'r'),(None,'x','r'))),
                             ((2,3),(('+',0,'r'),('x','q','s')))
                         ),
                         initial=1,
                         blank='_')

    mode = input('Step [s] or Runthrough [r]? ')
    step = mode.strip() == 's'
    run = create_terminal_runner(m, step=step)
    run()
    run = create_terminal_runner(m2, step=step)
    run()
