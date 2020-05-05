from os.path import join, dirname
from os import getcwd
# you should import all helper files here
from src.eda.example_helper_file import run_race_eda
# each helper file should have one or two functions that you call here those


def main(data_dir):
    # data dir will be set to any users Data directory if they put it at the top level of the project
    run_race_eda()
    print("hello")

if __name__ == '__main__':
    main(join(dirname(dirname(getcwd())), "Data"))