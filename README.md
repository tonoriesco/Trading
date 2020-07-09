[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

# Trading Test

Systematic Trading in python

[https://riesco.ch](Tono Riesco)

Version 0.4
2020-07-09

## Release notes v0.4

* Added a parameter file for loading data from a file in YAML format
* Added parameter to the command line for using or not the database when runnig the trades.
* Splited all the program in functions.
* Defined a strategy function in the program to isolate from the rest. In next versions will be readed from the file
* If DB is not used or the DB's are differents, several instances of the program can be runned in paralel.
* Concurrent work of paralel strategies with the database support.
* Recover the last values from the runs for each stock, index, forex pair, etc.

Version 0.2

2020-07-05

## Release notes v0.2

* Lots of improvements. New protocol and separation of funtions to help the new strategies.
* New version with database support.
* All the results are stored in a local database if needed for postprocessing.
* Now the pair is given in the command line.

## Description v0.2

**trading.py** is the open source version of my idea about the correct trading in terms of risk and take profit.
Currently working with a risk/reward of 1:2

Version 0.1

2020-07-04

## Release notes v0.1

First version

## Description v0.1

**trading.py** is the open source version of my idea about the correct trading in terms of risk and take profit.
Currently working with a risk/reward of 1:2
In future version all the parameters, pairs, etc. will be inputs from the user.
