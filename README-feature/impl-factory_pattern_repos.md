# Implementation of the Factory Pattern for repositories

## Here is what I have done

- Implemented the factory pattern for repositories (party_donation, party).
- Implemented e2e testing routes (**/v1/partydonations**, **/plugin/partydonations**, **/plugin/parties**).
- Refactored existing functions to fetch data for the routes with the repository factories.

## Description

I implemented the factory_pattern to handle multiple repositories. As long as unit tests, I wrote e2e tests for existing party donation-related routes. After checking the tests, I refactored the existing functions to fetch data (e.g., get_all_party_donations, get_parties) with repository factories.

(Before refactoring: partydonations)
e30a345 feat: Test plugin party_donation endpoint
95bf7c8 feat: Test pary_donation_v1 endpoint by postgres
a5b23ea feat: Set up env for testing

(After refactoring: partydonations)
6f246d4 feat: Replace with repo

(Before refactoring: parties)
0f0c8da feat: Restructure e2e testing
5450de6 feat: Test parties endpoint

(After refactoring: parties)
ba30cd7 feat: Replace with repo
