"""Handle arguments and run DCTM
"""

from curses import meta
from dctm import *
import yaml, json, argparse
from logging import error


parser = argparse.ArgumentParser(description='docker-compose template manager')
parser.add_argument('--config', '-c', type=str, nargs=1, 
                    help='path to variable configurations')
parser.add_argument('--template', '--temp', '--source', '-s', type=str, nargs=1,  
                    help='path to docketemplate, that we are overriding')
parser.add_argument('--destination', '--target', '-t', type=str, nargs=1,
                    help='path where docker-compose.yaml should be stored')
parser.add_argument('--strict', action='store_true',
                    help="Strictly check and compare values to template")

args = parser.parse_args()

def main():
    """Basic main function that will be executed
    """
    
    dctm = DCTM()
    
    strict = False
    if args.strict:
        strict = True
    
    dctm.switch(
        template_file=args.template[0],
        target_path=args.destination[0],
        template_values_dict=load_config(args.config[0]),
        strict=strict
    )

main()
