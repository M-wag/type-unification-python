from helpers import Substitution
from models import TypeVariable, TypeFunctionApplication
from test_models import test_monotypes_raw_to_C_and_mus

def main():
    x = TypeFunctionApplication(
        C = '->',
        mus = [TypeFunctionApplication('->', 
                                       [TypeVariable('a'), TypeFunctionApplication('->', 
                                            [TypeVariable('b'), 
                                             TypeVariable('c')])
                                            ]), 
               TypeVariable('c')]
    )


if __name__ == "__main__":
   test_monotypes_raw_to_C_and_mus()
