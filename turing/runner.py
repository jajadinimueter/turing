"""

"""

import sys
from blessings import Terminal
from turing.machine import compile_program


def create_terminal_runner(machine, step=False, loffset=15, roffset=None):
    roffset = roffset or loffset
    loffset = loffset or 15

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
                    c = ''.join(tape.format(format_char, loffset, roffset))
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
    m = machine.Machine(tapes=('000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000-000000000000000000000000000000000000000000000000000000000000000000000'),
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

    s_prog = '''
       [
         [(1,2), [(B,'S',R)]],
         [(2,3), [(B,'I',R)]],
         [(3,4), [(B,'V',R)]],
         [(4,5), [(B,'I',R)]],
         [(5,6), [(B,'\033[31m\u2764\033[37m',R)]],
         [(6,7), [(B,'F',R)]],
         [(7,8), [(B,'L',R)]],
         [(8,9), [(B,'O',R)]],
       ]  
    '''

    s_prog = compile_program(s_prog)

    any_prog = '''
        [
            [(1,1), [(A,A,R)]],
            [(1,2), [(1,1,S)]]
        ]
    '''

    any_prog = compile_program(any_prog)

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
    m3 = machine.Machine(tapes=('000000000000000000x000000000000', None), functions=prog)
    m4 = machine.Machine(tapes=(None,), functions=s_prog)

    mode = input('Step [s] or Runthrough [r]? ')
    step = mode.strip() == 's'

    #create_terminal_runner(m, step=step)()
    #create_terminal_runner(m3, step=step)()
    create_terminal_runner(
        machine.Machine(
            tapes=('00000001',),
            functions=any_prog
        ),
        step=step)()
    #create_terminal_runner(m4, step=step)()
