from os import getcwd
from os.path import join, dirname

from src.data_exploration import main_eda
from src.data_wrangling import main_wrangling
from src.modeling import main_modeling
from src.covid import covid_main


def main(args, data_dir=join((dirname(getcwd())), "Data")):
	"""
	Runs entire HFD Spring 2020 file. 
	"""
	print("---- Start Project ----")
	main_wrangling.main(data_dir, args)
	print("---- End Wrangling ----")
	main_eda.main(data_dir)
	print("---- End EDA ----")
	main_modeling.main(data_dir)
	print("---- End Modeling ----")
	covid_main.main(data_dir)
	print("---- Done ----")

if __name__ == "__main__":
    main()
