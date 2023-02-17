## ![Dive logo](https://user-images.githubusercontent.com/424487/219708981-f0416526-ba48-4b01-b5b3-c0eb73362718.png) Dive 
<!-- ![Company Logo](https://example.org) -->

### Company information

<!--- Use this section to share information about your company such as founding information, mission statement, product description, product success, etc.--->

### Why participate in an Octernship with Dive

<!--- Use this section to appeal to students. Consider sharing information about recent projects, the technology stack, the type of mentorship students can expect, listing future employment opportunities, etc. --->

### Octernship role description: Backend Engineering Intern

<!--- Use this section to describe the role in as much detail as necessary. Please include the GitHub Classroom assignment submission date, length of the Octernship, and the monthly stipend --->

### Recommended qualifications

<!--- Use this section to describe what skills a student might need to complete the problem statement on GitHub Classroom --->

### Eligibility

To participate, you must be:
* 18 years or older

## Assignment

# Write a REST API for the input of calories in Python

### Task Instructions
- API Users must be able to create an account and log in.
- All API calls must be authenticated.
- Implement at least three roles with different permission levels: a regular user would only be able to CRUD on their owned records, a user manager would be able to CRUD only users, and an admin would be able to CRUD all records and users.
- Each entry has a date, time, text, and number of calories.
- If the number of calories is not provided, the API should connect to a Calories API provider (for example, https://www.nutritionix.com) and try to get the number of calories for the entered meal.
- User setting – Expected number of calories per day.
- Each entry should have an extra boolean field set to true if the total for that day is less than the expected number of calories per day, otherwise should be false.
- The API must be able to return data in the JSON format.
- The API should provide filter capabilities for all endpoints that return a list of elements, as well should be able to support pagination.
- Write unit and e2e tests.
- Use any *Python* web framework
- Use *SQLite* as the database

### Task Expectations
- API Design Best Practices
- Documentation of any assumptions or choices made and why
- Unit tests covering the core calories logic
- Appropriate exception handling and error messages
- Code Quality - remove any unnecessary code, avoid large functions
- Good commit history - we won’t accept a repo with a single giant commit 🙅‍♀️

### Task submission
1. Use GitHub Classroom to make submissions.
1. Open a Pull Request for review.
1. Use GitHub Discussions to ask any relevant questions regarding the project.
1. Final submission Checklist:
- [ ] SUBMISSION.md in the repository / PR, with:
  - [ ] commands to set up the repo (dependencies etc.)
  - [ ] commands to run the test suite
  - [ ] commands to run the API server
