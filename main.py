from helpers import Substitution
from models import TypeVariable, TypeFunctionApplication, Context
from type_parser import type_parser, TypeParserTransformer
import lark
from test_w import test_w_examples

def main():
    tree = type_parser.parse('(Int)')
    print(tree)


if __name__ == "__main__":
    test_w_examples()

