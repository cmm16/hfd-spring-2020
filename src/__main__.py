from src.data_wrangling import main_wrangling
from src.data_exploration import main_eda
from src.modeling import main_modeling
from os.path import join, dirname
from os import getcwd


def main(data_dir=join((dirname(getcwd())), "Data")):
    main_wrangling.main(data_dir)
    print("done wrangling")
    main_eda.main(data_dir)
    print("done with eda")
    main_modeling.main(data_dir)
    print("done modeling")



if __name__ == "__main__":
    main()
