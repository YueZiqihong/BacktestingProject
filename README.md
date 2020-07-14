# BacktestingProject

## About this project
This project is designed to analyze the performance of trading strategies by simulating them in a virtual market. After the simulation, users can view their transactions in graphs to review the performance.

## Structure
/front contains front-end app using Vue.js
/analysisTool is the back-end app using django
Data are saved in reportdb.db locally.

## Dependencies
Node.js: https://nodejs.org/en/
Vue.js: $ npm install -g vue-cli
packages: element-ui, apache echarts, axios
django: $ python -m pip install Django
packages: numpy, pandas

## Insturctions
After setting up all dependencies, use
$ python manage.py runserver 
in command line at /analysisTool.
Then follow instuctions on command line to start the page.

## Special thanks
-The backtesting logics located at /analysisTool/testtools is contributed by Yiming Zhang. The external database file is a tool used for his testing use. He also controls how strategies are enacted.

-Contribution by Su Zhang to front end development, especially for stock pool displaying features.
