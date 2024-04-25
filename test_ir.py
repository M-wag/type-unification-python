import os
import sys

par_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parser_path = par_dir + "/Simple-Programming-Language-Python/"
prgm_path = par_dir + "/type-unification-python/demo_prgms"
sys.path.append(parser_path)

from spl_parser import spl_parser

def test_IR_CFG():

    # 
    pass 

