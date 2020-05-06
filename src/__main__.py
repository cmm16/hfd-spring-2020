from os import getcwd
from os.path import join, dirname

from src.data_exploration import main_eda
from src.data_wrangling import main_wrangling
from src.modeling import main_modeling
from src.covid import covid_main


def main(args, data_dir=join((dirname(getcwd())), "Data")):
    main_wrangling.main(data_dir, args)
    main_eda.main(data_dir)
    main_modeling.main(data_dir)
    covid_main.main(data_dir)


if __name__ == "__main__":
    main()
