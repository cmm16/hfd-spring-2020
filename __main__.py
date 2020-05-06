from src.__main__ import main
from os import path, getcwd

if __name__ == '__main__':
    main(data_dir=path.join(getcwd(), "Data"))
