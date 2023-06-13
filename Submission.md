# DiveHQ

Welcome to the DiveHQ Backend Internship Test! This guide will provide you with the necessary information to get started with the project.

This documentation provides an overview of the backend internship project, including instructions for setting it up locally. It also outlines the project workflow, scenario, and assumptions made during development. For a more detailed understanding, refer to the API documentation and review the project's code and database models.

## Documentation
To access the API documentation, please click [here](https://documenter.getpostman.com/view/22678038/2s93sf1W9p).

## Getting Started

Follow the steps below to set up the project on your local machine:

1. Clone the project repository by running the following command:
``` https://github.com/DiveHQ/backend-internship-task.git ```

2. Create a  virutal environment
``` python -m venv .venv ``` 
On Windows: Activate by:  ```.venv/scripts/activate```
On MacOS and Linux: Activate by:  ```source .venv/bin/activate```

3. Install dependencies
```pip install -r requirements.txt```

4. Run ``` python manage.py runserver ``` to server on port 8000 on local machine


## Project Workflow
### Scenario
An arbitrary user wants to track the amount of calories he takes in daily. As a backend developer, write an API in python to enable the user achieve the task

### Assumptions
I assumed that since the user wants to keep track of his daily calory intake, the user would have to set daily limts.
First of all, in a single day, the user cannot set more than one limits. 

There are three database models I used.

1. **User**: This table stores the details of the user and its role whether a Manager or Regular User
2. **Category Limit**: This table stores the daily calory limits of the user
3. **Calories**: This table stores the amount of calories and food taken. 

**The tables have a one-to-many-relationship between them**
