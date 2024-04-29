from jira import JIRA
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
# Your GitLab API endpoint and personal access token
jira_url = os.getenv('JIRA_URL')
token = os.getenv('JIRA_TOKEN')


# Connect to Jira instance
jira = JIRA(server=jira_url, token_auth=token)

# Define JQL query to get last updated issues
jql_query = 'project = LPEL23 order by updated desc'

# Search for issues
issues = jira.search_issues(jql_query, maxResults=10)  # Get the last 10 updated issues

# Print information for each issue
for issue in issues:
    print("Issue Key:", issue.key)
    print("Summary:", issue.fields.summary)
    print("Updated:", issue.fields.updated)
    print("----------------------------------")
