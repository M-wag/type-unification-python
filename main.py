from helpers import Substitution
from models import TypeVariable, TypeFunctionApplication


def main():
    x = TypeFunctionApplication('-> t1 -> t2 t3')
    print(x.mus)

if __name__ == "__main__":
    main()
