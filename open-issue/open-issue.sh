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
    --assignee $OPEN_ISSUE_ACTION_ASSIGNEE \
    --body "$theMessage" \
    --label "$OPEN_ISSUE_ACTION_LABEL" \
    --title "$OPEN_ISSUE_ACTION_NAME failed on $theDate"
else
  # comment on existing issue
  gh issue comment "$existing" \
    --body "$theMessage"
fi

echo "Success!"
