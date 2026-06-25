# Code Review Prompt

Use this prompt to review code generated with AI assistance.

```text
Review this change as a production engineer.

Focus on:
- correctness and edge cases;
- data leakage or privacy issues;
- model serving reliability;
- reproducibility;
- test coverage;
- operational risks;
- security risks;
- maintainability.

Return findings first, ordered by severity.
For each finding include:
- file and line;
- impact;
- suggested fix.
```

