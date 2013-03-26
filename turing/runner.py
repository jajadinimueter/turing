"""

"""

import sys
from blessings import Terminal
from turing.machine import compile_program


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
            sys.stdout.write(t.green(t.bold('[%s] ' % str(l + 1))))
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
    m = machine.Machine(tapes=('000000-00'),
                         functions=(
                             ((1,1),((0,0,'r'),)),
                             ((1,2),(('-',1,'r'),)),
                             ((2,2),((1,1,'r'),)),
                             ((2,3),((0,1,'l'),)),
                             ((3,3),((1,1,'l'),)),
                             ((3,2),((0,1,'r'),)),
                             ((2,4),((None,None,'l'),)),
                             ((4,4),((1,None,'l'),)),
                         ))

    prog = compile_program('''
        [
            [(1,2), [(0,1,R), (B,B,S)]],
            [(2,2), [(0,0,R), (B,B,S)]],
            [(2,3), [('x','x',R), (B,B,S)]],
            [(3,3), [(0,0,R), (B,0,R)]],
            [(3,4), [(B,B,L), (B,B,S)]],
            [(4,4), [(0,0,L), (B,B,S)]],
            [(4,5), [('x','x',L), (B,B,S)]],
            [(5,5), [(0,0,L), (B,B,S)]],
            [(5,1), [(1,1,R), (B,B,S)]],
            [(1,6), [('x','x',R), (B,B,S)]],
        ]
    ''')
    m3 = machine.Machine(tapes=('000000000000x0000', None), functions=prog)

    mode = input('Step [s] or Runthrough [r]? ')
    step = mode.strip() == 's'

    create_terminal_runner(m, step=step)()
    create_terminal_runner(m3, step=step)()