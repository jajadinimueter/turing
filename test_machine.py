"""

"""
import textwrap
import unittest
from turing import machine as ma
from turing.machine import compile_program

b = ' '

class TuringTestCase(unittest.TestCase):
    """

    """

    def test_uniary_plus(self):
        machine = ma.Machine(tapes=('00000+00',),
                                 functions=(
                                     ((1,2),((0,b,'r'),)),
                                     ((2,2),((0,0,'r'),)),
                                     ((2,3),(('+',0,'r'),))
                                 ),
                                 initial=1,
                                 blank=b)

        it = iter(machine)

        assert str(next(it)[1][0]) == '00000+00'
        assert str(next(it)[1][0]) == '0000+00'
        assert str(next(it)[1][0]) == '0000+00'
        assert str(next(it)[1][0]) == '0000+00'
        assert str(next(it)[1][0]) == '0000+00'
        assert str(next(it)[1][0]) == '0000+00'
        assert str(next(it)[1][0]) == '0000000'

        self.assertRaises(StopIteration, lambda: next(it))

    def test_uniary_minus(self):
        machine = ma.Machine(tapes=('00000-00',),
                                 functions=(
                                     ((1,1),((0,0,'r'),)),
                                     ((1,2),(('-',1,'r'),)),
                                     ((2,2),((1,1,'r'),)),
                                     ((2,3),((0,1,'l'),)),
                                     ((3,3),((1,1,'l'),)),
                                     ((3,2),((0,1,'r'),)),
                                     ((2,4),((b,None,'l'),)),
                                     ((4,4),((1,None,'l'),)),
                                 ),
                                 initial=1,
                                 blank=b)
        s = None
        for s in machine:
            pass
        assert str(s[1][0]) == '000'

    def test_compile_program(self):
        assert compile_program('''
            [
                [(1,1), [(1,B,R)]],
                [(1,2), [(B,B,R)]]
            ]
        ''') == [[(1, 1), [(1, None, 'r')]], [(1, 2), [(None, None, 'r')]]]

    def test_run_compiled_program(self):
        prog = compile_program('''
            [
                [(1,1), [(0,B,R)]],
                [(1,2), [(B,B,R)]]
            ]
        ''')
        m = ma.Machine(tapes=('00', ),
                       functions=prog)

        i = iter(m)
        assert str(next(i)[1][0]) == '00'
        assert str(next(i)[1][0]) == '0'
        assert str(next(i)[1][0]) == ''
        assert str(next(i)[1][0]) == ''

        self.assertRaises(StopIteration, lambda: next(i))

    def test_fac(self):
        fac = compile_program('''
            [
                [(1,2), [(0,1,R), (A,A,S), (B,0,R)]],
                [(2,2), [(0,0,R), (A,A,S), (B,0,R)]],
                [(2,3), [(B,B,L), (A,A,S), (B,B,L)]],
                [(3,3), [(0,0,S), (B,0,R), (0,0,L)]],
                [(3,4), [(0,0,L), (B,B,S), (B,B,R)]],
                [(3,6), [(1,1,R), (B,B,L), (B,B,R)]],
                [(4,4), [(0,0,S), (B,0,R), (0,0,R)]],
                [(4,3), [(0,0,L), (B,B,S), (B,B,L)]],
                [(4,5), [(1,1,R), (B,B,L), (B,B,L)]],
                [(5,5), [(0,0,R), (0,B,L), (A,0,L)]],
                [(5,5), [(B,B,S), (0,B,L), (A,0,L)]],
                [(5,4), [(B,B,L), (A,A,S), (B,B,R)]],
                [(5,4), [(B,B,L), (A,A,S), (B,B,R)]],
                [(6,6), [(B,B,S), (0,B,L), (A,0,R)]],
                [(6,3), [(B,B,L), (B,B,S), (B,B,R)]],
            ]
        ''')

        m = ma.Machine(tapes=('0000', None, None),
                       functions=fac)

        for i in m:
            print(i)

    def test_multiply(self):
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

        m = ma.Machine(tapes=('00x00', None),
                       functions=prog)
        i = iter(m)

        def n():
            _, tapes = next(i)
            t1, t2 = tapes
            return str(t1), str(t2)

        t1, t2 = n()
        assert str(t1) == '00x00'
        assert str(t2) == ''
        t1, t2 = n()
        assert str(t1) == '10x00'
        assert str(t2) == ''
        t1, t2 = n()
        assert str(t1) == '10x00'
        assert str(t2) == ''
        t1, t2 = n()
        assert str(t1) == '10x00'
        assert str(t2) == ''
        t1, t2 = n()
        assert str(t1) == '10x00'
        assert str(t2) == '0'
        t1, t2 = n()
        assert str(t1) == '10x00'
        assert str(t2) == '00'
        t1, t2 = n()
        assert str(t1) == '10x00'
        assert str(t2) == '00'
        t1, t2 = n()
        assert str(t1) == '10x00'
        assert str(t2) == '00'
        t1, t2 = n()
        assert str(t1) == '10x00'
        assert str(t2) == '00'
        t1, t2 = n()
        assert str(t1) == '10x00'
        assert str(t2) == '00'
        t1, t2 = n()
        assert str(t1) == '10x00'
        assert str(t2) == '00'
        t1, t2 = n()
        assert str(t1) == '10x00'
        assert str(t2) == '00'
        t1, t2 = n()
        assert str(t1) == '11x00'
        assert str(t2) == '00'
        t1, t2 = n()
        assert str(t1) == '11x00'
        assert str(t2) == '00'
        t1, t2 = n()
        assert str(t1) == '11x00'
        assert str(t2) == '000'
        t1, t2 = n()
        assert str(t1) == '11x00'
        assert str(t2) == '0000'
































