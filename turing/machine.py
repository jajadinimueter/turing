"""

"""
from ast import literal_eval
from collections import defaultdict
import re
import textwrap



DEFAULT_BLANK = '_'


class Any(object):
    """
    Marker for the any-char
    """


class Tape(object):
    def __init__(self, word=None, blank=DEFAULT_BLANK):
        self._blank = blank
        self._tape = {}
        self._pos = 0
        if word:
            for i, z in enumerate(word):
                self._tape[i] = z

    def __str__(self):
        return ''.join([x for x in self.format(lambda _,_1,c: c)
                        if x != self._blank])

    def chars(self, left_offset=None, right_offset=None):
        from_pos = 0
        to_pos = 0

        if left_offset is not None:
            from_pos = self._pos - left_offset
        else:
            from_pos = min(self._tape.keys() or [0])

        if right_offset is not None:
            to_pos = self._pos + right_offset + 1
        else:
            to_pos = min(self._tape.keys() or [0])

        result = []

        for i in range(from_pos, to_pos):
            result.append((self._pos, i, self._tape.get(i, self._blank)))

        assert len(result) == left_offset + right_offset + 1, "len(result) = %d. %d > %d. f: %d, t: %d. Pos: %d. Off: %d, %d" \
                                                                % (len(result),
                                                                   to_pos - from_pos,
                                                                   left_offset + right_offset,
                                                                   from_pos,
                                                                   to_pos,
                                                                   self._pos,
                                                                   left_offset, right_offset)

        return result

    def format(self, formatter, l=None, r=None):
        f = l and self._pos - l or min(self._tape.keys() or [0])
        t = r and self._pos + r or max(self._tape.keys() or [0])
        for i in range(f, t + 1):
            yield formatter(self._pos, i, self._tape.get(i, self._blank))

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
                 blank=DEFAULT_BLANK):
        """
        functions
        """

        if not tapes:
            tapes = []

        if type(tapes) not in (list, tuple, set):
            tapes = [tapes]

        self._tapes = {i : Tape(t, blank)
                       for i, t in enumerate(tapes)}

        self._blank = blank

        def r(t):
            t.pos += 1

        def l(t):
            t.pos -= 1

        transd = {
            'r': r, 'l': l, 's': lambda t: None}

        def mk_key(fns):
            lockey = []

            for tape_no, (cur_z, next_z, direction) in enumerate(fns):
                if cur_z is None:
                    cur_z = self._blank
                if type(cur_z) != bool:
                    cur_z = str(cur_z)
                lockey.append(cur_z)

            def checker(key):
                for i, dx in enumerate(lockey):
                    if dx is True:
                        break
                    if str(dx) != key[i]:
                        return False

                return True

            return checker

        self._functions = {}
        for (from_step, to_step), (fns) in functions:
            if str(from_step) not in self._functions:
                self._functions[str(from_step)] = defaultdict(list)
            tapes_key = mk_key(fns)
            for tape_no, (cur_char, next_char, direction) in enumerate(fns):
                if tape_no not in self._tapes:
                    self._tapes[tape_no] = Tape(blank=blank)
                if next_char is None:
                    next_char = self._blank
                if type(next_char) != bool:
                    next_char = str(next_char)
                self._functions[str(from_step)][tapes_key].append(
                    (next_char, str(to_step), transd[direction]))

        self._cur_tape = self.tapes[0]
        self._cur_state = str(initial)

    @property
    def tapes(self):
        return [self._tapes[i]
                for i in sorted(self._tapes.keys())]

    def __iter__(self):
        """
        Make the machine an iterator
        """
        yield self._cur_state, self.tapes
        next_step = self._next_step()
        while next_step:
            yield self._cur_state, self.tapes
            next_step = self._next_step()

    def _get_cur_transactions(self, key, transactions):
        for t, v in transactions.items():
            if t(key):
                return v

    def _next_step(self):
        """
        Calculate next step from input and functions
        """
        def mk_tape_key():
            l = []
            for t in self.tapes:
                l.append(t.read())
            return tuple(l)

        next_state = None
        transitions = self._functions.get(self._cur_state)
        tape_key = mk_tape_key()

        if transitions:
            cur_transitions = self._get_cur_transactions(tape_key, transitions)
            if cur_transitions:
                for tno, trans in enumerate(cur_transitions):
                    tape = self.tapes[tno]
                    if tape:
                        next_char, next_state, move = trans
                        if next_char is True:
                            next_char = tape.read()
                        tape.write(next_char)
                        move(tape)
                    else:
                        return False
            else:
                return False
        else:
            return False

        self._cur_state = next_state
        return True


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
    program = re.sub(r'([\s(,]+)A([\s,]+)', r'\1True\2', program)
    program = re.sub(r'([\s,]+)A([\s,]+)', r'\1True\2', program)
    program = re.sub(r'([\s,]+)R([)]+)', r'\1"r"\2', program)
    program = re.sub(r'([\s,]+)S([)]+)', r'\1"s"\2', program)
    program = re.sub(r'([\s,]+)L([)]+)', r'\1"l"\2', program)

    return literal_eval(textwrap.dedent(program))
