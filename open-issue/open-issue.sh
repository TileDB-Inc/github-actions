#!/bin/bash
set -e

# Open new Issue (or comment on existing)

if [[ -z "$GH_TOKEN" ]]
then
  echo "The env var GH_TOKEN is missing"
  echo "Please define it as a GitHub PAT with write permissions to Issues"
  exit 1
fi

theDate="$(date '+%A (%Y-%m-%d)')"
theMessage="The $OPEN_ISSUE_ACTION_NAME job failed on $theDate in run [$GITHUB_RUN_ID]($GITHUB_SERVER_URL/$GITHUB_REPOSITORY/actions/runs/$GITHUB_RUN_ID)"
echo "$theMessage"

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
  echo "Opening new issue"
  gh issue create \
    $flagAssignee \
    --body "$theMessage" \
    --label "$OPEN_ISSUE_ACTION_LABEL" \
    --title "The $OPEN_ISSUE_ACTION_NAME job failed on $theDate"
else
  echo "Commenting on existing issue"
  gh issue comment "$existing" \
    --body "$theMessage"
fi

echo "Success!"
