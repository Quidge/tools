# Purpose

Allows a group of people to rank multiple choices and see aggregate results.

## User flows

Two roles:

**Ballot creator:**

1. Enters a title and 2-8 choices
2. Distributes the ballot to participants
3. Collects each participant's response by name
4. If a duplicate name is entered, the previous response is replaced
5. Views results ranked by aggregate preference score, updated live as responses are added or removed

**Voter:**

1. Receives a ballot showing the title and choices
2. Ranks the choices in order of preference (can freely reorder before finalizing)
3. Receives a discrete artifact representing their ranking to return to the creator

> A ballot creator may also vote on their own ballot.

## Constraints

- Maximum of 8 choices per ballot
- Secrecy is of low importance — vote data is not designed to be private
