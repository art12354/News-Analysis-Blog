import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

def analyze_and_generate(transcript):
    """
    Analyze transcript for throughline topics and generate an essay and tags if found.
    """
    try:
        # Step 1: Analyze for a throughline topic
        throughline_analysis_prompt = f"""
        Analyze the following PBS NewsHour transcript and determine if there is a 
        significant throughline topic or theme. If no clear throughline exists, 
        respond with 'NO_THROUGHLINE'. If a significant topic exists, name it 
        specifically.

        Transcript:
        {transcript}
        """
        
        throughline_analysis = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": throughline_analysis_prompt}
            ]
        )
        
        throughline = throughline_analysis.choices[0].message.content.strip()
        
        # Normalize the throughline response for comparison
        if throughline.lower() == "no_throughline":
            return None, None, None

        # Step 2: Generate an essay about the identified throughline topic
        essay_generation_prompt = f"""
        Write a thoughtful essay about the following throughline topic from today's 
        PBS NewsHour episode: "{throughline}".

        Base the essay on this transcript:
        {transcript}

        Format the essay in markdown with:
        1. A compelling title
        2. An introduction connecting to today's news
        3. A substantive analysis of the topic
        4. A conclusion with broader implications

        The tone should be analytical and journalistic.
        """
        
        essay_generation = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": essay_generation_prompt}
            ]
        )
        
        essay_content = essay_generation.choices[0].message.content.strip()

        # Step 3: Generate tags from the essay content
        tags_generation_prompt = f"""
        Based on the following essay, generate a few suitable tags for a blog post. 
        Format the tags as a comma-separated list.

        Essay:
        {essay_content}
        """
        
        tags_generation = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": tags_generation_prompt}
            ]
        )
        
        tags = tags_generation.choices[0].message.content.strip().split(',')
        tags = [tag.strip() for tag in tags]

        return throughline, tags, essay_content

    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {e}")
        return None, None, None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, None, None

