from atlassian import Confluence
from requests.exceptions import HTTPError
import markdown2
import re
from plantweb.render import render_file
from urllib.parse import urlparse

from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()
# Your GitLab API endpoint and personal access token
confluence_url = os.getenv('CONFLUENCE_URL')
personal_access_token = os.getenv('CONFLUENCE_TOKEN')


# Connect to Confluence instance
confluence = Confluence(
    url=confluence_url,
    token=personal_access_token)

# Specify space key, title, and content
space_key = '~pyxa869'
title = 'api-docs-plantuml'
html_content = '<h1>Hello World!</h1>'
page=None
page_id=''
existing_page = confluence.get_page_by_title(space=space_key, title=title)
# If the page exists, use it
if existing_page:
    page = existing_page
    page_id=page['id']
else:
    # Create a new page
    page = confluence.create_page(space=space_key, title=title,body='')
    page_id = page['id']
try:

    with open('api-docs.md', 'r', encoding='utf-8') as file:
        markdown_content = file.read()
        pattern = r'``` plantuml (.*\.puml) ```'
        matches = re.findall(pattern, markdown_content)
        # Process each match
        for match in matches:
            # Extract filename
            filename = match

            # Render PNG file
            png_file = render_file(
                filename,
                renderopts={
                    'engine': 'plantuml',
                    'format': 'png'
                },
                cacheopts={
                    'use_cache': False
                }
            )

            # Replace occurrence of ``` plantuml filename.puml ``` with the path to the generated PNG file
            attachment = confluence.attach_file(page_id=page['id'], filename=png_file)
            # Get attachment URL
            attachment_url_download = attachment['_links']['download']
            parsed_url = urlparse(attachment_url_download)
            attachment_url = parsed_url.path
            # Replace occurrence of ``` plantuml filename.puml ``` with the attached image
            markdown_content = markdown_content.replace(f'``` plantuml {filename} ```',
                                                        f'![PlantUML Image]({attachment_url})')
            # Convert markdown content to HTML
            html_content = markdown2.markdown(markdown_content)
            print(html_content)

    # Create a new page
    # Update the Confluence page with HTML content
    htm="<p><img src='/download/attachments/341541182/seq.png' alt='PlantUML Image' /></p>"
    confluence.update_page(page_id=page_id, always_update=True, title=title, body=html_content, type='page')
    # Print the URL of the newly created page
    page_url = page['_links']['webui']
    print(f"Page created successfully: {page_url}")

except HTTPError as e:
    print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
except Exception as e:
    print(f"An error occurred: {e}")

