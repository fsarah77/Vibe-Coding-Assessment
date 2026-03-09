# REVIEW_NOTES

## 1. What happens if priority is provided in uppercase?
Observed behavior:
`POST /tasks` validates `priority` against an exact allowed set (`low`, `medium`, `high`, `critical`). Uppercase values like `HIGH` are rejected with `400 Bad Request`.

Risk / assessment:
This is strict and predictable, but clients sending uppercase variants will fail unless they normalize before calling the API.

Recommendation:
Keep strict validation if the API contract requires exact values. If client ergonomics are preferred, normalize with `priority.lower()` before validation and store canonical lowercase.

## 2. What happens if the title is 10,000 characters long?
Observed behavior:
The task is accepted as long as required fields are present/valid. There is no max length validation on `title`.

Risk / assessment:
Very long titles may cause memory growth, payload bloat, and downstream rendering/storage issues in real systems.

Recommendation:
Add explicit length validation (for example, `1..255` characters) and return `400 Bad Request` for out-of-range values.

## 3. Is user input properly sanitized?
Observed behavior:
`sanitize_input()` now removes script/style blocks, strips inline event handlers, and neutralizes `javascript:` patterns. `title` and `description` are sanitized before task creation.

Risk / assessment:
Sanitization is improved for common vectors but remains regex-based and not a complete HTML sanitizer. Complex payloads could still bypass simplistic rules.

Recommendation:
Use context-aware output escaping at render time and, when rich text is needed, a vetted sanitizer/allowlist approach instead of relying only on regex-based input cleanup.
