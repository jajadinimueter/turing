"""

"""
import argparse
import functools
import os

import sys
import time
import curses

from blessings import Terminal
from turing.machine import compile_program, Machine

def create_terminal_runner(machine,
                           step_by_step=False,
                           loffset=15,
                           roffset=None,
                           lag=0.1,
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
                screen.border(0)
                addstr(2,2,'[%s] ' % str(l + 1))
                with t.location(20):
                    addstr(2,10,'[State %s (%s)] ' % (str(cur_state), str(last_state)))
                for i, tape in enumerate(tapes):
                    addstr(i*2 + 2,25,'[Tape %s] ' % i)

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


def create_fast_runner(m, **kwargs):
    def run():
        c = 0
        for i, _ in enumerate(m):
            c += 1

        for tape in m.tapes:
            s = str(tape)
            print('%s: %s' % (len([x for x in s if x == '0']), s))

        print('Num steps: %d' % c)
    return run


def create_counter(char):
    def counter(chars, addstr):
        addstr('%d' % len([x for x in chars if x == char]))
    return counter


RUNNER_FACTORIES = {
    'pretty': create_terminal_runner,
    'fast': create_fast_runner
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('program')
    parser.add_argument('-i', '--input', dest='inputs', action='append')
    parser.add_argument('-o', '--output', dest='format')
    parser.add_argument('-s', '--step', action='store_true')
    parser.add_argument('-l', '--lag', type=float, dest='lag')
    parser.add_argument('-c', '--count', dest='count')

    args = parser.parse_args()

    file_path = os.path.abspath(os.path.expanduser(args.program))
    if not os.path.exists(file_path):
        # try current dir
        parser.exit(message='No such file %s\n' % file_path)

    with open(file_path, 'r', encoding='utf-8') as f:
        program = compile_program(f.read())

    kw = {'tapes': args.inputs}
    if isinstance(program, dict):
        kw.update(program)
    else:
        kw.update({'functions': program})

    ma = Machine(**kw)

    run_fac = RUNNER_FACTORIES.get(args.format)
    if not run_fac:
        run_fac = create_terminal_runner

    runargs = {
        'step_by_step': args.step,
        'lag': args.lag or 0.1
    }

    if args.count:
        runargs['tape_eval'] = create_counter(args.count)

    run_fac(ma,
            **runargs)()