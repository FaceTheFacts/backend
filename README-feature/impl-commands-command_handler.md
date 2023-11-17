# Implementation of Commands and Command Handler

## Here is what I have done

- Implemented commands and handlers.
- Tested them.

## Description

### Commands and Command Handlers Implementation

I have introduced a robust implementation of commands and corresponding command handlers, aligning with the principles discussed in [Chapter 10](https://www.cosmicpython.com/book/chapter_10_commands.html). This addition complements the previous branch where events were used to execute specific tasks. While events serve as broad broadcasters and are not directed to specific actors, commands are introduced as a more targeted replacement for events. Additionally, handlers are included to manage both events and commands as distinct types of messages.


## Potential Improvement
In this branch, the first step of fetching missing entities is executed manually. To enhance automation and efficiency, consider the following potential improvements:

1. Scheduled Execution: Utilize the schedule library to automate the periodic execution of the first step, fetching missing entities from the third-party API.

2. Event-Driven Architecture: Explore the implementation of a Redis Pub/Sub mechanism to further enhance the system's event-driven architecture, promoting decoupling and scalability.
