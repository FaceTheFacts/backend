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
   - Upon receiving the prepared data, Consumer 2 executes the final step to update the tables.

#### Execution Steps

1. **Initial State (Party Table):**

   - ![Party Table Before](images/party_table_before.png)

2. **Running Consumers:**

   - To run the pipeline, start Redis server and execute Consumer 1 and Consumer 2.
   - ![Running Consumers](images/running_consumers.png)

3. **Executing Publisher:**

   - Execute the event publisher to kickstart the pipeline.
   - ![Executing Publisher](images/executing_publisher.png)

4. **Updated State (Party Table and Party Style):**
   - ![Updated Party Table](images/updated_party_table.png)
   - ![Updated Party Style](images/updated_party_style.png)

### Automation and Future Improvements

The current implementation requires manual execution of the event publisher. To achieve full automation, consider using a scheduling library to automate the periodic execution of the publisher, ensuring consistent updates to the decoupled database and API.
