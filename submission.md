# Submission

Thank you for reviewing my solution. Here are the instructions to set up the repository, run the test suite, and start the API server.

## Repository Setup

1. Clone the repository:
git clone https://github.com/Abiorh001/backend-internship-task.git



2. Install the dependencies:
cd backend-internship-task

pip install -r requirements.txt



## Test Suite

To run the test suite, execute the following command:

pytest test_auth.py

pytest test_calories.py



The above command will discover and run all the tests in the repository. Make sure you have the necessary dependencies installed before running the tests.

## API Server

To start the API server, execute the following command:
uvicorn main:app --reload



The above command will start the server using the `main.py` file and enable auto-reloading for development purposes.

## API Documentation

Once the API server is running, you can access the API documentation using the following URL:
http://localhost:8000/docs

or you can access the full documentation using the following url:
http://localhost:8000/redoc



The API documentation provides detailed information about the available endpoints and request/response structures.

## Postman Collection

If you prefer to use Postman for testing the API, you can import the provided Postman collection (`calories_api.postman_collection.json`) into your Postman application. The collection contains pre-defined requests that you can use to interact with the API.

## Additional Notes

- Make sure to update the database connection settings in the `config.py` file to match your environment.
- The API server runs on port 8000 by default. If you need to change the port, you can modify the `uvicorn` command accordingly.
