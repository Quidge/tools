---
name: github-issue
description: >-
  Create GitHub Issues with the correct labels and formatting for this
  repository. Use when the user wants to create, file, open, log, or
  submit a GitHub issue, bug report, feature request, or enhancement
  request.
---

GitHub issues should follow a specific protocol.

### Labels

#### Narrowing to a specific tool

If the issue is about a specific tool, it should have a label designating which tool and type of tool it's for. Such as `<tool-type>:<tool-name>`.

Where `<tool-type>` may be ONE of: `bash`, `python`, or `html`. `<tool-name>` is the kebab case form of the name.

Example:
- `html:day-visualizer`

#### Narrowing down to a category of issue

- If the issue is for an enhancement, use the `enhancement` label
- If the issue is for a bug, use the `bug` label
- If the issue is for an investigation where it's unclear if the problem is a bug or a missing feature, use the `needs-investigation` label.

### Format

If possible, the issue should describe steps used to reproduce the behavior. If the issue is particularly visual in nature, take a screenshot and attach it.
