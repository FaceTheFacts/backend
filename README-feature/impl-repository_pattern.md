# Implementation of the Repository Pattern for Party Donation

## Here is what I have done

- Implemented the repository pattern for party donation.
- Conducted tests for the repository pattern.

## Description

I implemented the repository pattern for party donation table and test it.

## Missing

Refactoring party donation related routes (FastAPI routes) with the repository pattern. Plus, implementation of the repository pattern for other tables (e.g., Party, PartyDonationOrganization and etc).

## Potential Improvement

In the Architecture Patterns, the repository pattern (SQLAlchemyRepository) was implemented for just one table. But in reality, SQLAlchemyRepository must handle multiple tables. To manage multiple tables, abstract factory pattern (e.g., RepositoryFactory class) should be implemented.