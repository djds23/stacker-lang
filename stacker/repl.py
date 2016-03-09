import sys
from stacker.lang import Stacker

def repl():
    interpreter = Stacker()

    try:
        input = raw_input
    except NameError:
        pass

    while True:
        user_input = input('=>')
        if user_input == 'exit':
            sys.exit()

        interpreter.eval(user_input)
        print(interpreter.STACK)



