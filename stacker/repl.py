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

        try:
            interpreter.eval(user_input, interpreter.scope)
        except Exception as e:
            print(e)
        finally:
            print(list(interpreter.STACK))
            print(interpreter.scope)



