# Project Steps

- [x] **Setup Development Environment and Project Structure**

  - [x] Setup a Python virtual environment
  python3 -m venv flask-crud-venv
  source flask-crud-venv/bin/activate
  - [x] Create a suitable directory structure for the project
  {models, routes, services, tests}
  - [x] Install necessary Python package (Flask and SQLAlchemy)
  pip install flask sqlalchemy

- [x] **User Management**

  - [x] Implement user registration and login functionality
  - [x] Implement roles and permissions (regular user, user manager, admin)

- [x] **Data Model and Database**

  - [x] Design data model for entries (date, time, text, number of calories, boolean field for daily total comparison)
  - [x] Setup SQLite database and create tables according to the data model

- [ ] **Implement CRUD Operations**

  - [x] Implement Create, Read, Update, Delete operations for entries
  - [x] Implement Create, Read, Update, Delete operations for users (accessible by user manager and admin)

- [ ] **Integration with External Calories API**

  - [x] Connect to an external API to fetch calories if not provided

- [ ] **Implement User Settings**

  - [x] Allow users to set an expected number of calories per day

- [ ] **Boolean Field for Daily Calorie Comparison**

  - [x] Implement functionality to compare total daily calories with expected number and set boolean field accordingly

- [ ] **Implement Filtering, Pagination, and JSON Response Formatting**

  - [x] Add filter capabilities to endpoints returning a list of elements
  - [x] Add pagination to endpoints returning a list of elements
  - [x] Ensure all responses are formatted as JSON

- [ ] **Write Tests**

  - [x] Write unit tests to cover core calorie logic
  - [ ] Write end-to-end tests to validate overall functionality

- [ ] **Documentation and Code Quality**

  - [ ] Document assumptions, choices, and code references
  [SQLAlchemy V2](https://stackoverflow.com/questions/75365194/sqlalchemy-2-0-version-of-user-query-get1-in-flask-sqlalchemy)
  [Nutritionix API Wrapper](https://github.com/leetrout/python-nutritionix)
  [Flask Blueprint Testing](https://stackoverflow.com/questions/19962485/flask-blueprint-unit-testing)
  [Using Sqlite in Flask](https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application)

- [ ] **GitHub Flow**

  - [x] Create a new branch for the project
  - [ ] Raise a Pull Request for submission

- [ ] **Final Submission**
  - [ ] Create SUBMISSION.md with setup, test, and run commands

Note: urlparse has been changed to urllib.parse
In Nutritionx do
import urllib.parse




-[x] **Folder Structure**
.
├── README.md
├── create_tables.py
├── flask_crud
│   ├── __init__.py
│   ├── config.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── entry.py
│   │   ├── role.py
│   │   ├── setting.py
│   │   └── user.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── entry_routes.py
│   │   ├── setting_routes.py
│   │   └── user_routes.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── entry_service.py
│   │   └── user_service.py
│   ├── tests
│   │   ├── e2e
│   │   ├── functional
│   │   └── unit
│   │       ├── __init__.py
│   │       ├── __pycache__
│   │       ├── test_entry.py
│   │       └── test_user.py
│   └── utils
│       ├── __init__.py
│       └── helpers.py
├── progress.md
├── requirements.txt
└── run.py