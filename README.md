# Ticket Show Application - V2
## Description
This is a show/movie viewing web app built using Python-flask module for backend and Vue.js for frontend that allows the users to view and book tickets to shows.

The technologies used in this project include Flask extensions like Flask, request, redirect, url_for, render_template, current_app ; Flask-SQLAlchemy extensions like SQLAlchemy, flask_cors for cross origin resource sharing, Flask-JWT-Extended for Role Based Authentication, celery for executing backend jobs, redis for caching and queuing backend jobs, Flask-Caching for caching information and data from backend and matplotlib.


## Instructions and Information to run project
The python libraries listed in backend/requirements.txt must be installed, suggested in a virtual environment, before running the project.

The .sh file, local_run.sh is the main file to be executed. The allied code will be found in the folder application which are called during execution of the main file. cd to backend and run command 'sh local_run.sh'

The .sh file, local_workers.sh is the file that contains the run command for celery jobs. cd to backend and run command 'sh local_workers.sh'

The .sh file, local_c_beat.sh is the file that contains the run command for celery beat which is used for scheduling jobs. cd to backend and run command 'sh local_c_beat.sh'

The folder constraints frontend contains the frontend paart of the application. cd to the frontend and run command 'yarn serve'

## Project Interface

The project takes us to the url “/” which is where we choose to login as user or admin and the respective login happens. 

The CRUD for admin is with respect to managing shows and venues whereas for user is to make new registrations, book shows, give ratings and view past bookings. The user has an option to search for shows based on the location of venue and the tags associated with the show.


## Credits
This is an individually done project for the course of Modern Application Development II.