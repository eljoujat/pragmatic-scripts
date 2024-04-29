import gitlab
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
# Your GitLab API endpoint and personal access token
gitlab_url = os.getenv('GITLAB_URL')
personal_access_token = os.getenv('GITLAB_TOKEN')

gl = gitlab.Gitlab(url=gitlab_url, private_token=personal_access_token, keep_base_url=True)



def get_last_merge_request(project_id):
    project = gl.projects.get(project_id, lazy=True)
    mrs = project.mergerequests.list(state='merged', order_by='updated_at')
    for merge_request in mrs:
        print("Merge Request:")
        print(f"Author: {merge_request.author['name']} ({merge_request.author['username']})")
        print(f"Merge Date: {merge_request.merged_at}")
        print(f"Source Branch: {merge_request.source_branch}")
        print(f"Target Branch: {merge_request.target_branch}")
        print("----------------------------------")
# Replace 'YOUR_PROJECT_ID' with the ID of your GitLab project
project_id = "49"
last_merge_request = get_last_merge_request(project_id)

if last_merge_request:
    print("Last Merge Request:")
    print(f"Title: {last_merge_request['title']}")
    print(f"Author: {last_merge_request['author']['username']}")
    print(f"Created at: {last_merge_request['created_at']}")
    print(f"URL: {last_merge_request['web_url']}")
else:
    print("No merge requests found.")

