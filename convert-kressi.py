import ast
import sys

def convert(prog):
    transitions = []
    d = ast.literal_eval(prog)
    trans = d['transitions']
    yield '['
    def rep(x, mov=False):
        if mov:
            if x == 'n': return 'S'
            return x
        else:
            if x == '#': return 'B'
            return "'%s'" % x 
        
    for i, (k, v) in enumerate(trans.items()):
        if '-' not in k: continue
        if i < len(trans) and i != 0:
            yield ',\n' 
        fs, ft = k.split('-') 
        ts, tt = v.split('-') 
        yield '['       
        yield '(%s,%s), ' % (fs, ts)
        yield '['
        for tc in range(0, len(ft)):  # tape count
            if tc < len(ft) and tc != 0:
                yield ','
            yield '(%s,%s,%s)' % (rep(ft[tc]), rep(tt[tc]), rep(tt[tc+len(ft)], mov=True))
        yield ']'
        yield ']'
    yield ']'    

if __name__ == '__main__':
    for x in convert(sys.stdin.read()):
       sys.stdout.write(x)
