from helpers import Substitution
from models import TypeVariable, TypeFunctionApplication
from type_parser import type_parser, TypeParserTransformer
import lark

def main():
    tree = type_parser.parse('a')
    x = TypeParserTransformer().transform(tree)
    print(x)


if __name__ == "__main__":
    main()

