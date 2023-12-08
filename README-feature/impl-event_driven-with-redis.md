## Implementation of Event-Driven Architecture by Redis Pub/Sub

### Introduction

This README provides a comprehensive overview of the architecture and steps involved in leveraging Redis Pub/Sub to create a decoupled and efficient event-driven pipeline.

### What is Event-Driven Architecture?

Event-Driven Architecture is a design pattern where the flow of information between different components of a system is driven by events. This approach enables systems to react to changes in real-time, fostering seamless communication and updates.

### Why Redis Pub/Sub?

Redis Pub/Sub (Publish/Subscribe) is a messaging pattern that allows for the distribution of messages to multiple subscribers in a decoupled manner. It serves as a reliable and efficient choice for implementing event-driven systems. Redis Pub/Sub facilitates the asynchronous processing of events, enhancing the scalability and responsiveness of the system.

### Implementation Details

#### Utilising Redis Pub/Sub

This implementation follows the principles outlined in [Chapter 11](https://www.cosmicpython.com/book/chapter_11_external_events.html), introducing an event-driven pipeline powered by Redis Pub/Sub.

#### Workflow Overview

1. **Fetching Third-Party Data:**

   - Data fetching is initiated asynchronously by executing the FetchMissingEntity command.
   - The data is published to the "missing_entity_fetched" channel.

2. **Preparing Update Table Data:**

   - Consumer 1 (src/entrypoints/redis_eventconsumer_missing_entity_fetched.py) subscribes to the "missing_entity_fetched" channel.
   - Upon receiving a message, Consumer 1 executes the PrepareUpdateData command, preparing data for update tables.
   - The updated data is published to the "updated_entity_prepared" channel.

3. **Updating Tables:**
   - Consumer 2 (src/entrypoints/redis_eventconsumer_update_data_prepared.py) subscribes to the "updated_entity_prepared" channel.
   - Consumer 2 executes the final step to update the tables upon receiving the prepared data.

#### Execution Steps

1. **Initial State (Party Table):**
   <img width="1152" alt="before_party_table" src="https://github.com/FaceTheFacts/backend/assets/78789212/fede08e7-71a9-4f64-a9fc-acf45b5e7dab">

2. **Running Consumers:**

   - To run the pipeline, start Redis server and execute Consumer 1 and Consumer 2.
     <img width="1344" alt="running_only_consumer" src="https://github.com/FaceTheFacts/backend/assets/78789212/e4855ff9-0886-42fb-b222-f16b3727888a">

3. **Executing Publisher:**

   - Execute the event publisher to kickstart the pipeline.
     <img width="1333" alt="running_with_publisher" src="https://github.com/FaceTheFacts/backend/assets/78789212/d4797fe2-8df6-4528-974e-5beaa0a4dd1f">

4. **Updated State (Party Table and Party Style):**
   <img width="1126" alt="after_party_table" src="https://github.com/FaceTheFacts/backend/assets/78789212/e68b2ab5-a041-4e29-9ecf-f9fd674b545e">
   <img width="997" alt="after_party_style_table" src="https://github.com/FaceTheFacts/backend/assets/78789212/9e71daba-57bf-4c4e-9786-60f24e74ff8e">

### Automation

The event-driven pipeline is now fully automated using the `schedule` library. The scheduled tasks, including fetching missing entity data, preparing updated entity data, and publishing entity data, have been successfully implemented and integrated into the system.

- e.g., Run the tasks at 12:38.
