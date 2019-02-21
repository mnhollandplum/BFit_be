[![Waffle.io - Columns and their card count](https://badge.waffle.io/mnhollandplum/BFit_be.svg?columns=all)](https://waffle.io/mnhollandplum/BFit_be)

[![Build Status](https://travis-ci.org/mnhollandplum/BFit_be.svg?branch=master)](https://travis-ci.org/mnhollandplum/BFit_be)

![Heroku](https://heroku-badge.herokuapp.com/?app=heroku-badge)

## Contributing  
If you'd like to contribute to this project, fork this repository then follow the installation instructions below. Once you've finished the feature or fixes you wish to contribute, send us a pull request and one of us will review it before merging. If we have any suggestions, comments or questions we will leave them as comments on you pull request. Thank you in advance.

### Prerequisites/ Dependencies
 This project assumes you have installed:
 
 - [Python 3](https://realpython.com/installing-python/)
 
 - [Pip](https://pip.pypa.io/en/stable/reference/pip_install/)

### Installing

1. Clone down the repo:

`$ git clone git@github.com:mnhollandplum/BFit_be.git bfit_be`

2. Run:

`$ . venv/bin/activate # Activates virtual environment`

`$ pip install -r requirements.txt # Installs dependencies`

3. Setup the database:

`$ createdb bfit # Creates the postgresql database`

`$ flask db migrate # Creates a migration file`

`$ flask db upgrade # Runs the migration and creates all the tables`

## API Documentation
View all routes, requests, responses, and errors [here](./api_doc.md)

## MVP Schema<br/>
![Schema](./Schema.png)<br/>

## Known Issues

- Get test suite working and get test coverage up to %80
- Abstract and encapsulate repeated code into modules for easier reuse
- Add password hashing, user authentication and route authorization using access tokens
- Build out a more robust config file

## Next Steps
- Add tables and routes for posts to have workouts (with multiple exercises) and nutrition plans (with multiple meals)
- Add show route for each post
- Add functionality to sort your feed by popularity (based on awards) instead of most recent
- Pull in MyFitnessPal API data for foods and workouts (more research required)

## View Front End Implementation

[BFit Front End Repository](https://github.com/Cody-Price/BFit_fe)

### Contributors
[Tim Fell](https://github.com/TimothyFell)

[Nikki Holland-Plum](https://github.com/mnhollandplum)
