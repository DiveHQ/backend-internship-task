# Project Submission

## Repository Setup

1. Clone the repository:
   git clone

2. Change to the project directory:

cd <project_directory>

3. Create and activate a virtual environment (optional but recommended):

python -m venv env
source env/bin/activate # Linux/Mac
env\Scripts\activate # Windows

4. Install the project dependencies:
   pip install -r requirements.txt

## Running the Test Suite

1. Ensure that the virtual environment is activated (if applicable).

2. Run the unit and e2e tests:
   python manage.py test

## Running the API Server

1. Ensure that the virtual environment is activated (if applicable).

2. Apply database migrations:
   python manage.py migrate

3. Start the API server:
   python manage.py runserver

4. Access the API at `http://localhost:8000/`

Note: Replace `8000` with the appropriate port if you specified a different port.
