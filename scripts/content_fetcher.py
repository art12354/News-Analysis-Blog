import requests
from bs4 import BeautifulSoup
import datetime

def get_pbs_url(date_str):
    # Parse the date string into a datetime object
    date_obj = datetime.datetime.strptime(date_str, "%B-%d-%Y")
    
    # Check if it's a weekend (5 = Saturday, 6 = Sunday)
    is_weekend = date_obj.weekday() >= 5
    
    # Use "new-weekend" for weekends and "new-hour" for weekdays
    show_type = "weekend" if is_weekend else "hour"
    
    # Format the date for the URL with single digit for day when < 10
    month_name = date_obj.strftime("%B").lower()
    day = date_obj.day  # This will be an integer without leading zero
    year = date_obj.year
    
    formatted_date = f"{month_name}-{day}-{year}"
    
    # Construct the URL
    url = f"https://www.pbs.org/newshour/show/{formatted_date}-pbs-news-{show_type}-full-episode"
    
    return url

def fetch_pbs_transcript(date=None):
    """Fetch the PBS NewsHour transcript for a specific date"""
    if not date:
        date = datetime.datetime.now().strftime("%B-%d-%Y").lower()
    
    url = get_pbs_url(date)
    print(url)
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
       
        segments = soup.find_all('ul', class_='playlist')
        if segments:
            transcripts = []
            link_count = 0
            for segment in segments:
                links = segment.find_all('a', href=True)
                link_count = len(links)
                for link in links:
                    segment_url = link['href']
                    segment_response = requests.get(segment_url)
                    if segment_response.status_code == 200:
                        segment_soup = BeautifulSoup(segment_response.content, 'html.parser')
                        transcript = segment_soup.find('ul', class_='video-transcript')
                        if transcript:
                            transcripts.append(transcript.get_text())
            if len(transcripts) != len(links):
                raise ValueError("Transcript not yet released")
            cleaned_transcripts = "\n".join(transcripts).strip()
            return cleaned_transcripts
        raise ValueError("Unable to find segments on show page.")
    raise ValueError("Non 200 status code returned.")
