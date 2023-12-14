# Implementation of the Factory Pattern for repositories

## Here is what I have done

- Implemented the factory pattern for repositories (party_donation, party).
- Implemented e2e testing routes (**/v1/partydonations**, **/plugin/partydonations**, **/plugin/parties**).
- Refactored existing functions to fetch data for the routes with the repository factories.

## Description

I implemented the factory_pattern to handle multiple repositories. As long as unit tests, I wrote e2e tests for existing party donation-related routes. After checking the tests, I refactored the existing functions to fetch data (e.g., get_all_party_donations, get_parties) with repository factories.

(Before refactoring: partydonations)

```bash
e30a345 feat: Test plugin party_donation endpoint
95bf7c8 feat: Test pary_donation_v1 endpoint by postgres
a5b23ea feat: Set up env for testing
```

(After refactoring: partydonations)

```bash
6f246d4 feat: Replace with repo
```

(Before refactoring: parties)

```bash
0f0c8da feat: Restructure e2e testing
5450de6 feat: Test parties endpoint
```

(After refactoring: parties)

```bash
ba30cd7 feat: Replace with repo
```

## Potential Improvement

The current implementation for the updating tables(src/cron_jobs/utils/append_db.py) is highly coupled. For example, the `append_party` function combines multiple responsibilities, such as retrieving missing data from third-party and database updates, which violates SRP.

For testing and implementing an event-driven pattern, we should decouple the services.

1. Data Fetching Service:

- Fetch missing party data from the third-party API.
- Publish messages containing the retrieved data.

2. Database Update Service:

- Subscribe to the messages published by the data-fetching service.
- Process and update the database based on the received messages.
