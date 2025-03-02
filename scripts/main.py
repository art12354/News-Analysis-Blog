import os
from content_fetcher import fetch_pbs_transcript
from content_generator import analyze_and_generate
from file_creator import create_markdown_file
from git_manager import create_branch_and_pr
from dotenv import load_dotenv

load_dotenv()

def main():
    # Fetch today's transcript
    transcript = fetch_pbs_transcript()
    if not transcript:
        print("Couldn't fetch today's transcript")
        return
    
    # Analyze transcript and generate essay if throughline exists
    topic, tags, content = analyze_and_generate(transcript)
    if not topic:
        print("No significant throughline topic found today")
        return
    
    # Create markdown file
    filepath = create_markdown_file(topic, tags, content)
    print(f"Created file: {filepath}")
    
    # Create branch and PR
    success, pr_url = create_branch_and_pr(filepath, topic)
    
    if success and pr_url:
        print(f"Created pull request for review: {pr_url}")
    elif success:
        print("Created branch, but couldn't create PR automatically")
    else:
        print("Failed to create branch and PR")

if __name__ == "__main__":
    main()
