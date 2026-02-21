---
name: github-issue
description: Describes what to do when the user wants to create a new GitHub Issue 'or create an issue'. Details the correct labels and format to use.
---

Github issues should follow a specific protocol.

### Labels

#### Narrowing to a specific tool

If the issue is about a specific tool, it should should have a label designating which tool and type of tool it's for. Such as `<tool-type>:<tool-name>`.

Where `<tool-type>` may be ONE of: `bash`, `python`, or `html`. `<tool-name>` is the kebab case form of the name.

Example:
- `html:day-visualizer`

#### Narrowing down to a category of issue

- If the issue is for an enhancement, use the `enhancement` label
- If the issue is for a bug, use the `bug` label
- If the issue is for an investigation where it's unclear if the problem is a bug or a missing feature, use the `needs-investigation` label.

### Format

If possible, the issue should describe steps used to reproduce the behavior. If the issue is particularly visual in nature, provide screenshots.


