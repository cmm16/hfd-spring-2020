# HFD_Spring_2020
Team Houston Fire Department \
DSCI 435 Spring 2020 \
Rice University 


### Description 
<p align="center">
  <img src="images/healthmap.gif" height="350">
  <p align="center">Map of Block Group Health Call Proportions</p>
</p>

This is the repository for Team HFD's entire project. This set of scripts form a complete data science pipeline to create a general Risk Assessment and covid-19 risk assessment of Houston.

#### Methods Used 
- Time Series Decomposition
- Chi-squared tests
- Mann-Kendall trend test
- Light Gradient Boosting Model
- K-means clustering 

#### Technologies Used 
- Python 
   - NumPy/pandas
   - matplotlib 
   - scikit-learn
   - seaborn
   - folium 
- R 
   - NBClust 
   - Clustree

<p align="center">
  <img src="images/fdmap.gif" height="350">
   <p align="center">Toggleable Map of Call Proportions at Block Group and Fire District Level</p>
</p>

---
## Documentation 
[Full Report](https://drive.google.com/file/d/1lHDojuRc_ST6w6Wpj1SJOviPhoVKFqMl/view?usp=sharing)

### D2K Showcase 2020: Covid-19 Risk Assessment 
**People's Choice Winner**

[1 Minute Presentation Video](https://www.youtube.com/watch?v=amsAb2AAe24) \
[5 Minute Presentation Video](https://rice.app.box.com/s/qoxwjch1cir9ggsjkea5wj91gqmauir7)

---
## Getting Started 
Before getting started, make sure you are using at least conda version 3.8.2. 

### Set up virtual Environment
Follow the bellow instructions or copy and paste the commandline prompts under instructions
1. clone repo\
   `$ git clone https://github.com/cmm16/hfd-spring-2020.git;`\
  or if using ssh\
  `$ git clone git@github.com:cmm16/hfd-spring-2020.git;`
2. cd into base of project directory\
   `$ cd hfd-spring-2020;`
3. Prepare virtual environment\
If using mac, we recommend using: 
  `$ conda env create --file environment-all.yml`\
  `$ conda activate env`  (make sure this is the same command conda says to run)\
If using any other system, or if running into issues with command above, run:\
  `$ conda env create --file environment-light.yml`\
  `$ conda activate env` (make sure this is the same command conda says to run)\
  `conda install -c conda-forge pymannkendall shap folium bayesian-optimization`

After running our project, if you would like to deactivate the environment, type `$ conda deactivate`
   
### Download Data
Got to project box and download Data folder move to top level of this project\
The path to the data folder should now be "hfd-spring-2020/Data"

Unzip folder and make sure all contents go into folder called Data\
(on linux `unzip Data.zip`)

### Run
To run whole project (will take a lot of time)\
   `$ python $PWD;`

To run project but skip spatial join (saves time)\
   `$ python $PWD --skip True;`

After running the project, you can find general risk assessment outputs in "hfd-spring-2020/eda_output" and covid risk assessment outputs in "hfd-spring-20202/covid_output". 

---
### Members

<p align="center">
  <img src="images/team.jpg" width="500">
   <p align="center">Melinda Ding, Nick Falkenberg, Neyda Mami, Cole Morgan, Ohifeme Longe, Emre Yurtbay</p>
</p>
