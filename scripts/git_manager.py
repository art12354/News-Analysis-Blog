import subprocess
import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def create_branch_and_pr(filepath, topic):
    """Create a branch, commit article, push, and open a PR"""
    today = datetime.datetime.now().strftime("%B-%d-%Y")
    branch_name = f"article/{today}-{topic.lower().replace(' ', '-')[:30]}"
    
    # Get the repo info from environment variables
    github_token = os.environ.get("GITHUB_TOKEN")
    github_username = os.environ.get("GITHUB_USERNAME")
    github_repo = os.environ.get("GITHUB_REPO")
    
    # Create and checkout new branch
    commands = [
        ["git", "checkout", "-b", branch_name],
        ["git", "add", filepath],
        ["git", "commit", "-m", f"Add PBS NewsHour analysis: {topic} ({today})"],
        ["git", "push", "--set-upstream", "origin", branch_name]
    ]
    
    for cmd in commands:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error with command {' '.join(cmd)}")
            print(result.stderr)
            return False, None
    
    # Create pull request using GitHub API
    if github_token and github_username and github_repo:
        pr_url = create_pull_request(
            github_token, 
            github_username, 
            github_repo,
            branch_name,
            topic,
            today
        )
        return True, pr_url
    
    return True, None

def create_pull_request(token, username, repo, branch, topic, date):
    """Create a pull request using the GitHub API"""
    url = f"https://api.github.com/repos/{username}/{repo}/pulls"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "title": f"New PBS NewsHour Analysis: {topic} ({date})",
        "body": (
            f"This PR contains a new analysis article on '{topic}' from the "
            f"PBS NewsHour episode aired on {date}.\n\n"
            f"Please review the content for accuracy and editorial quality."
        ),
        "head": branch,
        "base": "main"
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code in (201, 200):
        return response.json()["html_url"]
    else:
        print(f"Failed to create PR. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None
