### Commands to set up the repo (dependencies etc.)
 > 1. Install dependencies with `pip install -r requirements/local.txt`.
  2. Create an `.env` file. Use `.env.sample` as a guide.
  3. Then run migrations with command `python manage.py migrate`.
  4. Create superuser with `python manage.py createsuperuser` and follow the prompt.
      - *You will need this to access the api docs. Its password protected*


  >*python version used `3.10`*

### Commands to run the test suite
  > To run tests with `pytest -rP` command


### Commands to run the API server
  >To start the server run `python manage.py runserver` 
  And run `localhost:8000` in the browser
  You can also access the admin page on `localhost:8000/admin`
  