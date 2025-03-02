import openai
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

def analyze_and_generate(transcript):
    """Analyze transcript for throughline topics and generate essay and tags if found."""
    
    # First determine if there's a significant throughline topic
    throughline_analysis_prompt = f"""
    Analyze this PBS NewsHour transcript and identify if there is a significant 
    throughline topic or theme. If there is no clear throughline, respond with 'NO_THROUGHLINE'.
    If there is a significant topic, name it specifically.
    
    Transcript:
    {transcript}
    """
    
    throughline_analysis = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": throughline_analysis_prompt}]
    )
    
    throughline = throughline_analysis.choices[0].message.content.strip()
    
    if throughline == "NO_THROUGHLINE":
        return None, None, None
    
    # Generate essay about the identified throughline topic
    essay_generation_prompt = f"""
    Create a thoughtful essay about the following throughline topic from today's 
    PBS NewsHour episode: "{throughline}"
    
    Base your essay on this transcript:
    {transcript}
    
    Format the essay in markdown with:
    1. A compelling title
    2. An introduction connecting to today's news
    3. A substantive analysis of the topic
    4. A conclusion with broader implications
    
    The tone should be analytical and journalistic.
    """
    
    essay_generation = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": essay_generation_prompt}]
    )
    
    essay_content = essay_generation.choices[0].message.content.strip()

    # Generate tags from the essay content
    tags_generation_prompt = f"""
    Find a couple tags that would be suitable to put on this blog post:
    {essay_content}
    
    Format the tags as a comma-separated list.
    """
    
    tags_generation = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": tags_generation_prompt}]
    )
    
    tags = tags_generation.choices[0].message.content.strip().split(',')
    tags = [tag.strip() for tag in tags]
    
    return throughline, tags, essay_content
