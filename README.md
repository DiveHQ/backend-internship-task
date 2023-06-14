<h3 align="center">CalorieIntake API</h3>

<div align="center">

</div>

---

<p align="center"> API for Calorie Intake
    <br> 
</p>

## 📝 Table of Contents
- [About](#about)
- [Assumptions](#assumptions)
- [Helpful Resources](#resources)
- [Built Using](#built_using)

## About <a name = "about"></a>
This is a REST API for tracking daily calorie intake. It is built using [these](#built_using) technologies.


## Assumptions <a name = "assumptions"></a>
In building this API, I made a number of assumptions
- The application has only one admin. This admin is created automatically when the application starts. The admin can create other either a manager or a user
- When an account is created, a user is given a default expected calories of 1000 per day
- The number of calories for a text is important. If a user does not enter the number of calories and the api call is also not able to retrieve the number of calories, an exception is raised. The user is then asked to enter the number of calories themselves or they enter a new text
- The user is given the chance to update a calorie entry including the number of calories field. If the user updates that, the is_below_expected field is recalculated to so we know if we are either below or above the expected calories for the day


## Helpful Resources <a name = "resources"></a>
These resources were helpful to me in completing the task
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy sum function](https://stackoverflow.com/questions/11830980/sqlalchemy-simple-example-of-sum-average-min-max)
- [Nutritionix Docs](https://docs.google.com/document/d/1_q-K-ObMTZvO0qUEAxROrN3bwMujwAN25sLHwJzliK0/edit#heading=h.h3vlpu5rgxy0)
- [Nutritionix API request](https://gist.github.com/mattsilv/6d19997bbdd02cf5337e9d4806b4f464)
- [Dependency management with poetry](https://realpython.com/dependency-management-python-poetry/)
- [Custom Exception handling in FastAPI](https://stackoverflow.com/questions/72831952/how-do-i-integrate-custom-exception-handling-with-the-fastapi-exception-handling/72833284#72833284)


## Built Using <a name = "built_using"></a>
- [FastAPI](https://fastapi.tiangolo.com/) - Python Framework
- [SQLite](https://www.sqlite.org/index.html/) - Database
- [Poetry](https://python-poetry.org/) - Python Package Manager
- [Docker](https://www.docker.com/) - Containerization
- [SqlAlchemy](https://www.sqlalchemy.org/) - ORM
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) - Database Migration
- [Pytest](https://docs.pytest.org/en/6.2.x/) - Testing Framework


