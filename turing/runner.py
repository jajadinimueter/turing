"""

"""
import functools

import sys
import time
import curses

from blessings import Terminal
from turing.machine import compile_program

def create_terminal_runner(machine,
                           step_by_step=False,
                           loffset=15,
                           roffset=None,
                           lag=0.02,
                           tape_eval=None):

    roffset = roffset or loffset
    loffset = loffset or 15

    def run():
        """


        """
        screen = curses.initscr()
        curses.start_color()
        screen.clear()
        screen.border(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)

        def addstr(*args, **kwargs):
            try:
                screen.addstr(*args,**kwargs)
            except curses.error:
                pass

        try:
            curses.noecho()
            curses.cbreak()
            local_step_by_step = step_by_step
            t = Terminal()
            last_state = None
            for l, (cur_state, tapes) in enumerate(machine):
                # screen.clear()
                # screen.border(0)
                # screen.addstr(t.green(t.bold('[%s] ' % str(l + 1))))
                addstr(2,2,'[%s] ' % str(l + 1))
                with t.location(20):
                    # stdscr.addstr(t.cyan(t.bold('[State %s] ' % str(cur_state))))
                    addstr(2,10,'[State %s (%s)] ' % (str(cur_state), str(last_state)))
                for i, tape in enumerate(tapes):
                    addstr(i*2 + 2,25,'[Tape %s] ' % i)

                    chars = ''
                    for j, (pos, cur, char) in enumerate(tape.chars(loffset, roffset)):
                        if pos == cur:
                            addstr(i* 2 + 2, j + 40, char, curses.color_pair(1))
                        else:
                            addstr(i* 2 + 2, j + 40, char)

                        if callable(tape_eval):
                            tape_eval(str(tape), functools.partial(addstr, i*2+2, 100))

                        screen.refresh()

                if local_step_by_step:
                    screen.getch()

                time.sleep(lag)
                screen.refresh()
                last_state = cur_state
            screen.getch()
        finally:
            curses.endwin()

    return run


def create_fast_runner(m):
    def run():
        c = 0
        for i, _ in enumerate(m):
            c += 1

        for tape in m.tapes:
            s = str(tape)
            print('%s: %s' % (len([x for x in s if x == '0']), s))

        print('Num steps: %d' % c)
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

    fac = compile_program('''
        [
            [(1,2), [(0,1,R), (A,A,S), (B,0,R)]],
            [(2,2), [(0,0,R), (A,A,S), (B,0,R)]],
            [(2,3), [(B,B,L), (A,A,S), (B,B,L)]],
            [(3,3), [(0,0,S), (B,0,R), (0,0,L)]],
            [(3,4), [(0,0,L), (B,B,S), (B,B,R)]],
            [(3,6), [(1,1,R), (B,B,L), (0,0,S)]],
            [(3,6), [(1,1,R), (B,B,L), (B,B,L)]],
            [(4,4), [(0,0,S), (B,0,R), (0,0,R)]],
            [(4,3), [(0,0,L), (B,B,S), (B,B,L)]],
            [(4,5), [(1,1,R), (B,B,L), (0,0,S)]],
            [(5,5), [(0,1,S), (0,B,L), (A,0,R)]],
            [(5,5), [(1,1,S), (0,B,L), (A,0,R)]],
            [(5,7), [(1,1,R), (B,B,S), (B,B,S)]],
            [(7,7), [(0,0,R), (B,B,S), (B,B,S)]],
            [(7,3), [(B,B,L), (B,B,S), (B,B,L)]],
            [(6,6), [(0,1,S), (0,B,L), (A,0,L)]],
            [(6,6), [(1,1,S), (0,B,L), (A,0,L)]],
            [(6,8), [(1,1,R), (B,B,S), (B,B,S)]],
            [(8,8), [(0,0,R), (B,B,S), (B,B,S)]],
            [(8,4), [(B,B,L), (B,B,S), (B,B,R)]],
        ]
    ''')

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
    # create_terminal_runner(m3, step_by_step=step)()
    # create_terminal_runner(
    #     machine.Machine(
    #         tapes=('00000001',),
    #         functions=any_prog
    #     ),
    #     step_by_step=step)()

    def print_0_counts(tape_content, addstr):
        addstr('%s' % len([x for x in tape_content if x == '0']))

    fac_machine =  machine.Machine(
        tapes=('000000000',None,None),
        functions=fac
    )

    # create_terminal_runner(
    #     fac_machine,
    #     step_by_step=step,
    #     lag=0,
    #     tape_eval=print_0_counts)()

    create_fast_runner(fac_machine)()

    #create_terminal_runner(m4, step=step)()
