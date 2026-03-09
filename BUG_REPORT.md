# BUG_REPORT

## tests/test_utils.py::TestSanitizeInput::test_removes_script_variations
Expected behavior:
Script variations (including uppercase tags) should not leave executable script content.

Actual behavior:
`<SCRIPT>alert('xss')</SCRIPT>` was not sanitized correctly; `alert` remained.

Root cause:
Sanitization only removed exact lowercase `<script>` and `</script>` tokens, case-sensitively, and did not remove block content robustly.

Fix applied:
Updated `sanitize_input()` to remove full script/style blocks using case-insensitive regex with DOTALL.

## tests/test_utils.py::TestSanitizeInput::test_removes_img_onerror
Expected behavior:
Inline event handlers such as `onerror=` should be removed.

Actual behavior:
`onerror` attribute remained unchanged.

Root cause:
No logic existed to strip `on*` event handler attributes.

Fix applied:
Added case-insensitive regex removal for inline event handler attributes (e.g., `onerror`, `onclick`).

## tests/test_utils.py::TestSanitizeInput::test_removes_javascript_url
Expected behavior:
`javascript:` URI schemes should be removed/neutralized.

Actual behavior:
`javascript:` remained in sanitized output.

Root cause:
No handling for dangerous URI schemes.

Fix applied:
Added case-insensitive `javascript:` neutralization in `sanitize_input()`.
