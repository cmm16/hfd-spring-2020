# HFD_Spring_2020
DSCI 435 project repo for team Houston fire department Spring 2020
---
### How to Run this Project
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
   `$ pipenv shell;`\
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

To run project on smaller dataset (saves time)\
`$ pipenv run python $PWD --small True;`
