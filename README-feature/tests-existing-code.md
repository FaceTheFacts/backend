# Party Donation Related Tables Testing

## Here is what I have done

- Conducted unit tests for Party, PartyDonation, and PartyDonationOrganization tables using SQLite.
- Conducted unit tests for get_all_party_donations used by **/partydonations**.

## Description

In preparation for the implementation of an event-driven pipeline for updating party donation information, I conducted tests on party donation related tables. This ensures the data integrity of Party, PartyDonation, and PartyDonationOrganization tables and lays the foundation for future updates.

## Missing

Testing for populating tables (inserting and updating the database by scraped data) is currently missing. We plan to complete this functionality in the near future.

## Potential Improvement

To enhance the testability of our functions, we can consider decoupling functions and addressing dependency injection. This will make our code more modular and easier to test.
