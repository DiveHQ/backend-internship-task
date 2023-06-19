# Backend Internship Task Submission

## Code Overview

The code in this repo implements a Flask-based REST API for managing calorie entries. It provides routes for user registration, authentication, creating calorie entries, setting expected calorie per day and retrieving specific calorie entries.

The code consists of the following files and folders:

1. `flask_crud/models`: Contains the database models and schema.
2. `flask_crud/routes`: Contains the routes
3. `flask_crud/config.py`: Configuration file with various settings.
4. `flask_crud/tests`: Contains the test files with various settings.
5. `create_tables.py`: Script to setup and configure the database, however, running the app (after setting your db_url and other config variables) sets it up either ways.
6. `requirements.txt`: File listing the required dependencies and their versions.


## Usage Instructions

To run the application locally, follow these steps:

0. Initialize the python venv by running `python3 -m venv new_venv`
- activate it with `source new_venv/bin/activate`
1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Rename `.env.example` to `.env` and put your own details.
3. Generate the database by running `python create_tables.py`.
4. Start the Flask application by running `flask run`.
5. Run the tests with `python -m unittest flask_crud.tests.unit.test_user`
6. The application will be accessible at `http://localhost:4747`.
7.When you're done working in the virtual environment, you can deactivate it by running the deactivate command `deactivate`

## Dependencies

The project's major dependencies are:

- Flask==2.3.2
- Flask-SQLAlchemy==3.0.0
- requests==2.31.0

The other dependencies are specified in the `requirements.txt` file.


## Author

The code in this repository was written by Maestroh1Git (David Amaku).