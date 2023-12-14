# Implementation of events and the message bus

## Here is what I have done

- Implemented the message bus to execute events.
- Implemented pipeline to fetch missing and update tables (in this branch I focused on party table)
- Tested the pipeline

## Description

### Message Bus Implementation
I have implemented a message bus based on the principles discussed in [Chapter 8](https://www.cosmicpython.com/book/chapter_08_events_and_message_bus.html) and [Chapter 9](https://www.cosmicpython.com/book/chapter_09_all_messagebus.html). The message bus is designed to facilitate the execution of events within the system.

### Pipeline for Fetching and Updating Tables

**Step 1: Fetch Missing Entity from Third-party API**

The first step involves manually fetching missing entities from a third-party API, specifically the abgeordnetenwatch API. This step is executed manually and can be found in the src/service_layer/utils.py file.

- Reference: src/service_layer/utils.py

**Step 2: Prepare Data for Insertion**

This step focuses on preparing data for insertion into tables. For instance, when fetching party items from the third-party API, party_style IDs are prepared for the Party table, which requires party_style IDs as foreign keys.

- Reference: src/service_layer/handlers.py/prepare_update_data

**Step 3: Update Tables**

The final step involves updating tables based on the prepared data.

- Reference: src/service_layer/handlers.py/update_table

## Potential Improvement
In this branch, the first step of fetching missing entities is executed manually. To enhance automation and efficiency, consider the following potential improvements:

1. Scheduled Execution: Utilize the schedule library to automate the periodic execution of the first step, fetching missing entities from the third-party API.

2. Command Integration: Introduce commands in addition to events to enhance flexibility in executing various tasks within the system.

3. Event-Driven Architecture: Explore the implementation of a Redis Pub/Sub mechanism to further enhance the system's event-driven architecture, promoting decoupling and scalability.
