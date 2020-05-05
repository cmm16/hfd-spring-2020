from src.data_wrangling import main_wrangling
from os.path import join, dirname
from os import getcwd


def main(data_dir=join((dirname(getcwd())), "Data")):
    main_wrangling.main(data_dir)


if __name__ == "__main__":
    main()
