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
                           lag=None,
                           tape_eval=None):

    roffset = roffset or loffset
    loffset = loffset or 15

    def run():
        """


        """

        with open('/tmp/turing.log', 'w') as log:
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
                last_pos = {}

                old_curs = {}
                forward_counts = {}
                backward_counts = {}

                for step_count, (cur_state, tapes) in enumerate(machine):
                    screen.move(2,2)
                    screen.clrtoeol()
                    screen.border(0)
                    addstr('[%s] ' % str(step_count + 1))

                    with t.location(20):
                        addstr(2,10,'[State %s (%s)] ' % (str(cur_state), str(last_state)))

                    for i, tape in enumerate(tapes):
                        if tape not in forward_counts:
                            forward_counts[tape] = 0
                        if tape not in backward_counts:
                            backward_counts[tape] = 0
                        if tape not in old_curs:
                            old_curs[tape] = 0

                        cur = 0
                        j = 0
                        x = i*2 + 10
                        y = 25
                        screen.move(x, y)
                        screen.clrtoeol()
                        addstr(x, y,'[Tape %s] ' % i)

                        for j, (pos, cur, char) in enumerate(tape.chars(loffset, roffset)):
                            log.write('%s\n' % j)

                            if pos == cur:
                                addstr(x, y + 30 + j, char, curses.color_pair(1) | curses.A_BOLD)
                            else:
                                if j == 0:
                                    addstr(x, y + 30 + j, char)
                                else:
                                    addstr(x, y + 30 + j, char, curses.A_BLINK)

                            if callable(tape_eval):
                                tape_eval(str(tape), functools.partial(addstr, x, y + 10))

                        if tape.pos > last_pos.get(i,0):
                            forward = '.'
                            forward_count = forward_counts[tape]

                            if forward_count == 2:
                                forward = '..'
                            if forward_count == 4:
                                forward = '...'
                            if forward_count == 6:
                                forward = '....'
                                forward_counts[tape] = 0

                            addstr(x, y + 30 - len(forward), forward, curses.A_BOLD)

                            if cur > old_curs[tape]:
                                backward_counts[tape] = 0
                                forward_counts[tape] += 1
                        elif tape.pos < last_pos.get(i,0):
                            backward = '.'
                            backward_count = backward_counts[tape]

                            if backward_count == 2:
                                backward = '..'
                            if backward_count == 4:
                                backward = '...'
                            if backward_count == 6:
                                backward = '....'
                                backward_counts[tape] = 0

                            addstr(x, y + j + 30, backward, curses.A_BOLD)
                            if cur < old_curs[tape]:
                                forward_counts[tape] = 0
                                backward_counts[tape] += 1
                        else:
                            forward_counts[tape] = 0
                            backward_counts[tape] = 0

                        last_pos[i] = tape.pos
                        old_curs[tape] = cur

                    if local_step_by_step:
                        screen.getch()

                    if lag:
                        time.sleep(lag)

                    last_state = cur_state

                    screen.refresh()

                screen.getch()
            finally:
                curses.endwin()

    return run


def create_fast_runner(m, tape_eval=None, **kwargs):
    def run():
        c = 0
        for i, _ in enumerate(m):
            c += 1

        # for tape in m.tapes:
        #     print('%s', str(tape))

        if callable(tape_eval):
            for tape in m.tapes:
                tape_eval(str(tape), lambda x: print(x))

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
        'lag': args.lag
    }

    if args.count:
        runargs['tape_eval'] = create_counter(args.count)

    run_fac(ma,
            **runargs)()
