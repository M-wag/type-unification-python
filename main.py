from helpers import Substitution
from models import TypeVariable, TypeFunctionApplication, Context
from type_parser import type_parser, TypeParserTransformer
import lark
from test_w import test_

def main():
    tree = type_parser.parse('a')
    x = TypeParserTransformer().transform(tree)
    print(x)


if __name__ == "__main__":
    test_()

