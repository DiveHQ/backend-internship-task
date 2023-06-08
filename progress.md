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

  - [ ] Implement Create, Read, Update, Delete operations for entries
  - [x] Implement Create, Read, Update, Delete operations for users (accessible by user manager and admin)

- [ ] **Integration with External Calories API**

  - [ ] Connect to an external API to fetch calories if not provided

- [ ] **Implement User Settings**

  - [ ] Allow users to set an expected number of calories per day

- [ ] **Boolean Field for Daily Calorie Comparison**

  - [ ] Implement functionality to compare total daily calories with expected number and set boolean field accordingly

- [ ] **Implement Filtering, Pagination, and JSON Response Formatting**

  - [ ] Add filter capabilities to endpoints returning a list of elements
  - [ ] Add pagination to endpoints returning a list of elements
  - [ ] Ensure all responses are formatted as JSON

- [ ] **Write Tests**

  - [ ] Write unit tests to cover core calorie logic
  - [ ] Write end-to-end tests to validate overall functionality

- [ ] **Documentation and Code Quality**

  - [ ] Document assumptions, choices, and code references

- [ ] **GitHub Flow**

  - [x] Create a new branch for the project
  - [ ] Raise a Pull Request for submission

- [ ] **Final Submission**
  - [ ] Create SUBMISSION.md with setup, test, and run commands
