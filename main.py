from helpers import Substitution
from models import TypeVariable, TypeFunctionApplication
from test_models import test_type_parser as test


def main():
    x = TypeFunctionApplication('-> t1 -> t2 t3')
    print(x.mus)

if __name__ == "__main__":
   test()
