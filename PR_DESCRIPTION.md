## Summary of the Implementation

This Pull Request completes the required assessment tasks across Parts 2, 3, and 4.

Implemented features:
- Added `POST /tasks` endpoint with validation for required fields
- Added validation for `priority` values: `low`, `medium`, `high`, `critical`
- Added user existence check before task creation
- Added unique task ID generation for new tasks
- Added `GET /tasks` support for filtering by:
  - `user_email`
  - `status`
  - `priority`
- Added `GET /tasks` support for sorting by:
  - `priority_score`
  - `due_date`
  - `created_at`
- Added `REVIEW_NOTES.md` for the required security review questions
- Added `BUG_REPORT.md` documenting utility-related test failures and fixes

## List of Bugs Fixed

The following utility bugs were identified and fixed:
- `validate_email()`
- `calculate_priority_score()`
- `sanitize_input()`
- `parse_date()`

Additional fixes:
- Correct handling of invalid task input
- Correct response codes for bad requests and missing users
- Task filtering and sorting behavior aligned with the assessment requirements

## AI Tool(s) Used

The following AI tools were used during the assessment:
- ChatGPT
- Codex

## Reflection on Where AI Was Helpful and Where It Failed

AI was helpful for:
- breaking down the assessment into a clear implementation plan
- generating endpoint scaffolding
- suggesting validation logic
- helping structure markdown documentation
- speeding up debugging by narrowing down likely causes of failing tests

AI was less reliable when:
- interpreting repository-specific behavior without checking the existing codebase
- assuming implementation details that were not guaranteed by the project structure
- suggesting generic fixes that still needed manual verification against the tests

Because of that, all AI suggestions were manually reviewed and adjusted based on the actual repository code and test results.