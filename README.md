# HFD_Spring_2020
Team Houston Fire Department \
DSCI 435 Spring 2020 \
Rice University \

---
## Documentation 

#### D2K Showcase 2020: Covid-19 Risk Assessment 
**People's Choice Winner**
[1 Minute Presentation Video](https://www.youtube.com/watch?v=amsAb2AAe24) 
[5 Minute Presentation Video](https://rice.app.box.com/s/qoxwjch1cir9ggsjkea5wj91gqmauir7)

---
## Getting Started 
Before starting, make sure your python is at least version 3.7.5 and that you have pip installed. 

#### Set up virtual Environment
Follow the bellow instructions or copy and paste the commandline prompts under instructions
1. clone repo\
   `$ git clone https://github.com/cmm16/hfd-spring-2020.git;`\
  or if using ssh\
  `$ git clone git@github.com:cmm16/hfd-spring-2020.git;`
2. cd into base of project directory\
   `$ cd hfd-spring-2020;`
3. Prepare virtual environment\
  `$ pip install pipenv;`\
   `$ pipenv sync;`
   
#### Download Data
Got to project box and download Data folder move to top level of this project\
The path to the data folder should now be "hfd-spring-2020/Data"

Unzip folder and make sure all contents go into folder called Data\
(on linux `unzip Data.zip`)

#### Run
To run whole project (will take a lot of time)\
`$ pipenv run python $PWD;`

To run project but skip spatial join (saves time)\
`$ pipenv run python $PWD --skip True;`

After running the project, you can find general risk assessment outputs in "hfd-spring-2020/eda_output" and covid risk assessment outputs in "hfd-spring-20202/covid_output". 
