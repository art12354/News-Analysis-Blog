import os
import datetime

def create_markdown_file(topic, tags, content):
    """Create a markdown file with proper frontmatter for Hugo"""
    today = datetime.datetime.now()
    date_str = today.strftime("%B-%d-%Y")
    slug = topic.lower().replace(" ", "-").replace(",", "").replace(":", "")[:40]
    
    frontmatter = f"""---
title: "{topic}"
date: {date_str}
draft: false
tags: {tags}
---

"""
    
    full_content = frontmatter + content
    
    # Create directory if it doesn't exist
    os.makedirs("content/posts", exist_ok=True)
    
    # Write file
    filename = f"content/posts/{date_str}-{slug}.md"
    with open(filename, "w") as f:
        f.write(full_content)
    
    return filename
