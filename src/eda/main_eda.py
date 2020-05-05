from os.path import join, dirname
from os import getcwd

def main(data_dir):
    # data dir will be set to any users Data directory if they put it at the top level of the project

    print("hello")

if __name__ == '__main__':
    main(join(dirname(dirname(getcwd()))), "Data")