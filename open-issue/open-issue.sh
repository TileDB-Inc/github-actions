#!/bin/bash
set -ex

# Open new Issue (or comment on existing)

if [[ -z "$GH_TOKEN" ]]
then
  echo "The env var GH_TOKEN is missing"
  echo "Please define it as a GitHub PAT with write permissions to Issues"
  exit 1
fi

theDate="$(date '+%A (%Y-%m-%d)')"
theMessage="$OPEN_ISSUE_ACTION_NAME failed on $theDate in run [$GITHUB_RUN_ID]($GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID)"

# --assignee flag is optional
if [[ -n "$OPEN_ISSUE_ACTION_ASSIGNEE" ]]
then
  flagAssignee="--assignee $OPEN_ISSUE_ACTION_ASSIGNEE"
else
  flagAssignee=""
fi

existing=$(gh issue list \
  --label "$OPEN_ISSUE_ACTION_LABEL" \
  --limit 1 \
  --jq '.[].number' \
  --json "number" \
  --state "open")

if [[ -z "$existing" ]]
then
  # open new issue
  gh issue create \
    $flagAssignee \
    --body "$theMessage" \
    --label "$OPEN_ISSUE_ACTION_LABEL" \
    --title "$OPEN_ISSUE_ACTION_NAME failed on $theDate"
else
  # comment on existing issue
  gh issue comment "$existing" \
    --body "$theMessage"
fi

# Save the Issue number as output
issueNumber=$(gh issue list \
  --label "$OPEN_ISSUE_ACTION_LABEL" \
  --limit 1 \
  --jq '.[].number' \
  --json "number" \
  --state "open")
echo "issue-number=$IssueNumber" >> $GITHUB_OUTPUT

echo "Success!"
