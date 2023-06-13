# Calorie Tracker API

REST API for managing and tracking daily calorie intake.

## Setting up the project

1. Clone the repository:

   ```bash
   git clone git@github.com:snnbotchway/calorie-tracker.git
   ```

2. Navigate to the Django project's directory:

    ```bash
    cd calorie-tracker/calorie_tracker
    ```

    Verify that you are in the correct directory by running the `ls` command. You should see `manage.py` among the listed files.

3. Create a `.env` file by duplicating the provided `.env.example` file:

   ```bash
   cp .env.example .env
   ```

4. If you haven't already, download and set up Docker. Alternatively, you can use a virtual environment.

5. Build a Docker image with all the project dependencies by running the following command:

    ```bash
    docker compose build
    ```

6. If using a virtual environment, install the dependencies with `pip install -r requirements/local.txt`

## Running the Test suite

1. Ensure that you are in the Django project directory (verify `manage.py` is listed when running `ls`).

2. Run the tests using Docker:

    ```bash
    docker compose run --rm web sh -c pytest
    ```

    If you are using a virtual environment, simply run `pytest`.

## Running the API server

1. Verify that you are in the Django project directory (check for `manage.py` after running `ls`).

2. Start the server using Docker:

    ```bash
    docker compose up
    ```

    If you are using a virtual environment, run `python3 manage.py runserver`.
