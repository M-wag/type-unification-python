from helpers import Substitution
from models import TypeVariable, TypeFunctionApplication

def main():

    tv = TypeFunctionApplication(
                C = '->',
                mus = [
                        TypeFunctionApplication(
                            C = '->',
                            mus = [TypeVariable('a'), TypeVariable('b')]),
                        TypeFunctionApplication(
                            C = 'List',
                            mus = [TypeFunctionApplication('Int', mus=[])]),
                    ]
                )

    print(tv)


if __name__ == "__main__":
    main()

