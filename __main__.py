from src.__main__ import main
from os import path, getcwd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--small', help='Boolean on whether to run on smaller data set')
parser.add_argument('--skip', help='Boolean on whether skip geospatial join')

args = parser.parse_args()

if __name__ == '__main__':
    main(vars(args), path.join(getcwd(), "Data"))
