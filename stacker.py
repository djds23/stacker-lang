# coding: utf-8
# http://beautifulracket.com/first-lang.html
import re
from collections import deque
from functools import wraps

class Procedure (object):
    def __init__(self, inp):
        self.inp = inp

    def expression_list(self):
        return map(lambda s: s.strip(), self.inp[1:-1].split(';'))

class FuncMixin(object):
    def void_function(self, f):
        @wraps(f)
        def wrapper(*args):
            if any(args):
                raise StackerArgumentError('{} takes no arguments'
                                           ' but void'
                                           .format(f.__name__))
            return f(*args)
        return wrapper

class Stacker (FuncMixin):
    STACK = deque()

    def stack_head(self):
        try:
            value = self.STACK[0]
        except IndexError:
            value = None
        return value

    def env(self):

        def _not(*args):
            value = self.STACK.popleft()
            if value is False:
                self.STACK.appendleft(True)
            else:
                self.STACK.appendleft(False)
            return self.STACK

        def _or (*args):
            value1 = self.STACK.popleft()
            value2 = self.STACK.popleft()
            if value1 is False or value2 is False:
                self.STACK.appendleft(False)
            else:
                self.STACK.appendleft(True)
            return self.STACK

        def _eq(*args):
            other = args[0]
            value = self.STACK.popleft()
            out = other == value
            self.STACK.appendleft(out)
            return self.STACK

        def rot(*args):
            value = self.STACK.popleft()
            self.STACK.append(value)
            return self.STACK

        def over(*args):
            value = self.stack_head()
            self.STACK.append(value)
            return self.STACK

        def drop(*args):
            self.STACK.popleft()
            return self.STACK

        def swap(*args):
            value1 = self.STACK.popleft()
            value2 = self.STACK.popleft()
            self.STACK.appendleft(value1)
            self.STACK.appendleft(value2)
            return self.STACK

        def dup(*args):
            value = self.stack_head()
            self.STACK.appendleft(value)
            return self.STACK

        def push(*args):
            self.STACK.appendleft(args[0])
            return self.STACK

        return {
            'push': push,
            'drop': drop,
            'dup': dup,
            'swap': swap,
            'over': over,
            'rot': rot,
            'eq': _eq,
            'or': _or,
            'not': _not
        }

    def parser(self, inp):
        if inp.startswith('{') and inp.endswith('}'):
            return Procedure(inp)
        if len(inp) == 0:
            return None
        funcs = '(' + '|'.join(self.env().keys()) + ')'
        matcher = re.compile('{} (\d+|\w+)'.format(funcs))
        expression = matcher.match(inp)
        if not expression:
            print inp
            raise StackerSyntaxError('invalid syntax: {}'.format(inp))
        return map(self.atomizer, expression.group(0).split())

    def atomizer(self, atom):
        try:
            value = int(atom)
        except ValueError:
            value = str(atom)
            if value == 'void':
                value = None

            if value == 'false':
                value = False

            if value == 'true':
                value = True

        return value

    def eval(self, inp):
        parsed_inp = self.parser(inp)
        if isinstance(parsed_inp, Procedure):
            for exp in parsed_inp.expression_list():
                atoms = self.parser(exp)
                self.eval_exp(atoms)
        else:
            self.eval_exp(parsed_inp)



    def eval_exp(self, atoms):
        if atoms is None:
            return None

        func = self.env().get(atoms[0], None)
        return func(*atoms[1:])

class StackerSyntaxError (Exception):
    pass

class StackerArgumentError (Exception):
    pass

class StackerTypeError (Exception):
    pass

class StackEatenUp (Exception):
    pass

def test():
    s = Stacker()
    s.eval('push 1')
    s.eval('push 2')
    assert s.STACK == deque([2, 1])
    print 'pass 1'

    s.eval('swap void')
    assert s.STACK == deque([1, 2])
    print 'pass 2'

    s.eval('push 3')
    s.eval('rot void')
    assert s.STACK == deque([1, 2, 3])
    print 'pass 3'

    s.eval('drop void')
    assert s.STACK == deque([2, 3])
    print 'pass 4'

    s.eval('over void')
    assert s.STACK == deque([2, 3, 2])
    print 'pass 5'

    s.eval('drop void')
    assert s.STACK == deque([3, 2])
    print 'pass 6'

    s.eval('eq 3')
    assert s.STACK == deque([True, 2])
    print 'pass 7'

    s.eval('or void')
    assert s.STACK == deque([True])
    print 'pass 8'

    s.eval('not void')
    assert s.STACK == deque([False])
    print 'pass 9'

    # anon funcs
    s.eval('{drop void; push 9; push 9;}')
    print s.STACK

test()
