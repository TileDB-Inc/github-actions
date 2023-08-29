# Open GitHub Issue

Insert this action into your GitHub Actions workflow to automatically open an
Issue from a GitHub Actions job (or comment on an existing open Issue). This
requires that the default GitHub token in the job has write permissions to
Issues.

Usage notes (see `action.yml` for more details):

* The required argument `name` is used in the Issue title and body
* The required argument `label` is used to identify an existing open Issue to
  comment on. Thus the label (or combination of labels) must be specific to this
  auto-opened Issue. If you were to only use a generic label like `bug`, then
  the action would comment on the most recent Issue with that label. To use a
  new unique label, you must manually create it on the repository first. Trying
  to use a non-existing label with this action will result in an error
* The argument `assignee` is optional. If you list any users that do not have
  write-access to the repository, then they will simply be ignored
* You don't need to explicitly pass the GitHub token to the action. This is
  already automatically done by the action. The only requirement is that you set
  `issues: write` in the `permissions`. While you could set this permission for
  the entire workflow, it's best practice to limit the escalated authentication
  for only the job(s) that require it

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
          name: nightly build
          label: bug,nightly-failure
          assignee: username
```

Notes on the example:

* Requests the GitHub token to have permission to write to Issues (the minimum
  scope required for this action)
* Can run on macOS, Ubuntu, and Windows runners
* Assumes the job above that might fail is named "build"
* Only opens the Issue if the job "build" fails or is cancelled
* Only opens the Issue if the job was scheduled
* If there is an existing open Issue with the labels `bug` and
  `nightly-failure`, the action will comment on this Issue instead of opening a
  new one
