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

   Set the `NUTRITIONIX_APP_ID` and `NUTRITIONIX_APP_KEY` in the `.env` file if you wish to test the fetching of calories from the provider(Nutritionix). You can get them at __<https://developer.nutritionix.com/admin/access_details>__.

4. If you haven't already, download and set up Docker. Alternatively, you can use a virtual environment.

5. If using Docker, build a Docker image with all the project dependencies by running the following command:

    ```bash
    docker-compose build
    ```

    If you are using a virtual environment, create and activate the virtual environment:

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

    Then, install the dependencies with `pip`:

    ```bash
    pip install -r ../requirements/local.txt
    ```

## Running the Test suite

1. Ensure that you are in the Django project directory (verify `manage.py` is listed when running `ls`).

2. If using Docker, run the tests inside a Docker container:

    ```bash
    docker-compose run --rm web sh -c pytest
    ```

    If you are using a virtual environment, simply run `pytest`.

## Running the API server

1. Verify that you are in the Django project directory (check for `manage.py` after running `ls`).

2. If using Docker, start the API server using Docker Compose:

    ```bash
    docker-compose up
    ```

    If you are using a virtual environment, start the server with the following command:

    ```bash
    python3 manage.py runserver
    ```

    The API server will be accessible at `http://127.0.0.1:8000/`.
