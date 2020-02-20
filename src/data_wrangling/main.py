from os import path
from os import getcwd
from src.data_wrangling.cad_wrangling import cad_wrangling
from src.data_wrangling.spatial_join import spatial_join
from src.data_wrangling.aggregate import aggregate


def main():
    data_dir = path.join(path.dirname(path.dirname(getcwd())), "data")
    inc_save_path = path.join(data_dir, "inc_cad_clean.csv")
    # unit_save_path = path.join(data_dir, "unit_cad_clean.csv")

    cad_wrangling(data_dir, inc_save_path, inc_type="inc", unzip=True)
    # cad_wrangling()
    # spatial_join()
    # aggregate()


if __name__ == "__main__":
    main()
