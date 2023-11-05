# Here is What I have done.

- Added Pylint.
- Generated a UML.
- Analysed the UML.
- Proposed potential improvement.

# Description

In this branch, I automatically generated a UML by [Pyreverse](https://pylint.readthedocs.io/en/latest/pyreverse.html) underling Pylint to analyse existing structures.

# UML

Since the generated UML is huge (1.2MB), I stored it in Google Drive.

Here is the [link](https://drive.google.com/file/d/1X8WbZdDZLS34gVqFH47N0_pWty6tRQ66/view).

# Analysis

This analysis provides an overview of the structure and design patterns used in the "Face The Facts" project. The project primarily employs the FastAPI framework for its web functionality and SQLAlchemy for database management. Additionally, the project adheres to a functional programming paradigm, except in cases where FastAPI schemas and database models require a different approach.

## FastAPI Schemas

The project leverages FastAPI for web-related functionality, particularly in defining schemas. These schemas inherit from either the FTFBaseModel class or the BaseModel class from the Pydantic library. This choice depends on the specific requirements of the schema and its usage within the project.

## Database Classes

Database management in the project relies on SQLAlchemy. All database classes inherit from the Base class provided by SQLAlchemy. This inheritance ensures consistency in database modeling and allows for efficient data manipulation and querying.

# Potential Improvement

## Repository patterns

In the current implementation of the project's crud.py module, database operations are handled directly within the functions. While this approach can work effectively for smaller projects, a more structured and scalable approach could be to adopt the Repository Pattern.

Here is benefits:

1. Abstraction: It provides an abstraction layer between the application code and the database, making it easier to switch databases or data sources if needed.

2. Testability: With data access logic decoupled from business logic, unit testing becomes more straightforward, as you can mock the repository for testing purposes.

3. Maintainability: Changes to the data access layer can be isolated, reducing the impact on the rest of the codebase.

4. Flexibility: Different implementations of repositories can be used for different data sources (e.g., databases, APIs).
