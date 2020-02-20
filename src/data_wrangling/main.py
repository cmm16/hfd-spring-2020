from src.data_wrangling.cad_wrangling import cad_wrangling
from src.data_wrangling.spatial_join import spatial_join
from src.data_wrangling.aggregate import aggregate


def main():
    cad_wrangling()
    spatial_join()
    aggregate()


if __name__ == "__main__":
    main()
