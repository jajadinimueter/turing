"""

"""
from ast import literal_eval
from collections import defaultdict
import re
import textwrap


class Tape(object):
    def __init__(self, word=None, blank=' '):
        self._blank = blank
        self._tape = {}
        self._pos = 0
        if word:
            for i, z in enumerate(word):
                self._tape[i] = z

    def __str__(self):
        return ''.join([x for x in self.format(lambda _,_1,c: c)
                        if x != self._blank])

    def format(self, formatter, l=None, r=None):
        f = l and self._pos - l or min(self._tape.keys())
        t = r and self._pos + r or max(self._tape.keys())
        for i in range(f, t+1):
            yield formatter(self._pos, i, self._tape.get(i,self._blank))

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, p):
        self._pos = p

    def write(self, val):
        self._tape[self._pos] = val

    def read(self):
        return self._tape.get(self._pos, self._blank)

class Machine(object):
    def __init__(self,
                 tapes,
                 functions,
                 initial=1,
                 blank=' '):
        """
        functions
        """

        if not tapes:
            raise ValueError('tapes')

        if type(tapes) not in (list,tuple,set):
            tapes = [tapes]

        self._tapes = [Tape(t, blank) for t in tapes]
        self._blank = blank

        def r(t):
            t.pos += 1
        def l(t):
            t.pos -= 1

        transd = {
            'r': r, 'l': l, 's': lambda t: None}

        self._functions = {}
        for (f, t), (fns) in functions:
            if str(f) not in self._functions:
                self._functions[str(f)] = defaultdict(dict)
            for tape_no, (cur_z, next_z, direction) in enumerate(fns):
                if cur_z is None:
                    cur_z = self._blank
                if next_z is None:
                    next_z = self._blank
                self._functions[str(f)][tape_no][str(cur_z)] = (str(next_z), str(t), transd[direction])

        self._cur_tape = tapes[0]
        self._cur_state = str(initial)

    def __iter__(self):
        """
        Make the machine an iterator
        """
        yield self._cur_state, self._tapes
        n = self._next_step()
        while n:
            yield self._cur_state, self._tapes
            n = self._next_step()

    def _next_step(self):
        """
        Calculate next step from input and functions
        """
        done = False
        transitions = self._functions.get(self._cur_state)
        if transitions:
            for tno, tape in enumerate(self._tapes):
                cur_z = tape.read()
                t_transitions = transitions.get(tno)
                if t_transitions:
                    trans = t_transitions.get(cur_z)
                    if trans:
                        next_z, next_state, move = trans
                        tape.write(next_z)
                        move(tape)
                        self._cur_state = next_state
                        done = True
        return done


def compile_program(program):
    """

    Program must be in form:
        [
            ((step_from, step_to), [(tape1_input, tape1_output, tape1_direction),
                                  (tape2_input, tape2_output, tape2_direction)])
            ((step_from, step_to), [(tape1_input, tape1_output, tape1_direction),
                                  (tape2_input, tape2_output, tape2_direction)])
        ]

    Example:
        {
            functions=[
                ((1,1), [(1,    B,'r'),
                         (0,    1,'l)],
                # ...
            ]
        }
    """

    # replace blanks with None
    program = re.sub(r'([\s,(]+)BLANK([\s,]+)', r'\1None\2', program)
    program = re.sub(r'([\s(,]+)B([\s,]+)', r'\1None\2', program)
    program = re.sub(r'([\s,]+)B([\s,]+)', r'\1None\2', program)
    program = re.sub(r'([\s,]+)R([)]+)', r'\1"r"\2', program)
    program = re.sub(r'([\s,]+)L([)]+)', r'\1"l"\2', program)

    return literal_eval(textwrap.dedent(program))
