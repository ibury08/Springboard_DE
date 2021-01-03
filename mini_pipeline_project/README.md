# Mini-pipeline Project
The goal for this project was to write a python script to insert the values of a csv into a mysql table, run an aggregation query, and return the results to the user via stdout.

## Run with Docker
Instead of setting up a local mysql server to insert into, we can just run with Docker. `docker-compose.yml` creates a mysql container and runs the python script `mini.py` in another container.
`git clone git@github.com:ibury08/Springboard_DE.git && cd Springboard_DE/mini_pipeline_project && docker-compose up`
CTRL+C to exit when done.

## Run with Python
<b>Note</b>: This script assumes you have 1) MySQL server running 2) updated the config in lines 10-14 in mini.py and 3) created the database 'sales'. 
The abstraction to allow a user to pass in their config is a v1.5 feature.
