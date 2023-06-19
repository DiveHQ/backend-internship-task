# Backend Internship Task Submission

## Code Overview

The code in this repository implements a Flask-based REST API for managing calorie entries. It provides routes for user registration, authentication, creating calorie entries, and retrieving specific calorie entries.

The code consists of the following files:

1. `api.py`: Contains the main Flask application and routes.
2. `config.py`: Configuration file with various settings.
3. `generate_db.py`: Script to generate and configure the database.
4. `requirements.txt`: File listing the required dependencies and their versions.

## Commits

The code development was organized into several commits, with each commit introducing specific changes and improvements. Here is a summary of the commits:

1. Commit 1: Initial project setup with basic Flask application.
2. Commit 2: Defined database models for User and CalorieEntry.
3. Commit 3: Implemented user registration route.
4. Commit 4: Implemented user login route and JWT token generation.
5. Commit 5: Added route for creating calorie entries.
6. Commit 6: Implemented helper functions for calculating total calories and expected calories.
7. Commit 7: Added get_entry route to retrieve a specific calorie entry.
8. Commit 8: Defined helper functions for extracting user ID and fetching calories from an API.
9. Commit 9: Added main function to run the Flask application.
10. Commit 10: Added a configuration file with secret key, database URI, and CORS settings.
11. Commit 11: Created a script to generate the database.

## Usage Instructions

To run the application locally, follow these steps:

1. Install the required dependencies by running `pip install -r requirements.txt`.
2. Generate the database by running `python generate_db.py`.
3. Start the Flask application by running `python api.py`.
4. The application will be accessible at `http://localhost:5000`.

## Dependencies

The project depends on the following packages:

- Flask==2.1.0
- Flask-SQLAlchemy==3.0.0
- requests==2.26.0

These dependencies are specified in the `requirements.txt` file.

## Future Improvements

Here are some potential improvements that could be made to the code:

- Implement additional routes for updating and deleting calorie entries.
- Implement pagination for retrieving multiple calorie entries.
- Add validation and error handling for input data.
- Implement user roles and permissions for more fine-grained access control.
- Implement unit tests for the application logic.


I noticed that the code is currently encountering an error. The specific error message indicates a problem with the database configuration in the api.py file. It seems that the database URL specified in the code is either missing or incorrect, causing the SQLAlchemy initialization to fail.

To fix this issue, you need to provide a valid database URI in the config.py file. Make sure the URI is correct and points to a running database instance. Additionally, ensure that you have the necessary database drivers installed for the chosen database system.

## Instructions to fix the code issue later:

To resolve the database configuration issue and make the code work, please follow these steps:

- Open the config.py file.
- Locate the SQLALCHEMY_DATABASE_URI variable and ensure it contains the correct URI for your database system.
- If you're using a local database, the URI might look like this: sqlite:///path/to/database.db.
- If you're using a remote database, consult your database provider's documentation to obtain the correct URI format.
- Save the changes to the config.py file.

## Author

The code in this repository was written by Om Bhojane.

