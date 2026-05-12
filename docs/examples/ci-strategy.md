# CI Strategy

Public CI on GitHub or Codeberg should focus on:

- YAML parse checks
- profile resolution checks
- compile smoke tests
- small public runtime workflows

CERN GitLab can extend this with:

- private-data workflows
- heavier runtime validation
- long-running comparisons

Private data should not be required for public CI.
