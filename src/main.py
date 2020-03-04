from src.data_wrangling import main_wrangling
from os import path
from os import getcwd


def main(data_dir=path.join((path.dirname(getcwd())), "test_data")):
    main_wrangling.main(data_dir)


if __name__ == "__main__":
    main()
