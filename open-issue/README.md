# Open GitHub Issue

Insert this action into your GitHub Actions workflow to automatically open an
Issue from a GitHub Actions job (or comment on an existing open Issue). This
requires that the default GitHub token in the job has write permissions to
Issues.

Example:

```yaml
  issue:
    permissions:
      issues: write
    runs-on: ubuntu-latest
    needs: build
    if: ( failure() || cancelled() ) && github.event_name == 'schedule'
    steps:
      - uses: actions/checkout@v3
      - name: Open Issue
        uses: ./open-issue
        with:
          name: Nightly build
          label: bug
          assignee: username
```

Notes on the example:

* Requests the GitHub token to have permission to write to Issues (the minimum
  scope required for this action)
* Can run on macOS, Ubuntu, and Windows runners
* Assumes the job above is named "build"
* Only opens the Issue if the job "build" fails or is cancelled
* Only opens the Issue if the job was scheduled
