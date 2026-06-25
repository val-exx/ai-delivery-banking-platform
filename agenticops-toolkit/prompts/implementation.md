# Implementation Prompt

Use this prompt when asking an AI coding assistant to implement a scoped feature.

```text
You are working in an existing repository. First inspect the relevant files and infer local conventions.

Task:
<describe the feature or fix>

Constraints:
- keep the change scoped;
- prefer existing patterns and helpers;
- add or update tests for the changed behavior;
- avoid unrelated refactors;
- document only non-obvious decisions.

Before editing:
- list the files you expect to touch;
- explain the expected behavior;
- mention risks or assumptions.

After editing:
- summarize the changes;
- list verification commands and results;
- identify any remaining limitations.
```

