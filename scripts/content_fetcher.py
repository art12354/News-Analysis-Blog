import requests
from bs4 import BeautifulSoup
import datetime

def fetch_pbs_transcript(date=None):
    """Fetch the PBS NewsHour transcript for a specific date"""
    if not date:
        date = datetime.datetime.now().strftime("%B-%d-%Y").lower()
    
    url = f"https://www.pbs.org/newshour/show/{date}-pbs-news-hour-full-episode"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
       
        segments = soup.find_all('ul', class_='playlist')
        if segments:
            transcripts = []
            for segment in segments:
                links = segment.find_all('a', href=True)
                for link in links:
                    segment_url = link['href']
                    segment_response = requests.get(segment_url)
                    if segment_response.status_code == 200:
                        segment_soup = BeautifulSoup(segment_response.content, 'html.parser')
                        transcript = segment_soup.find('ul', class_='video-transcript')
                        if transcript:
                            transcripts.append(transcript.get_text())
            cleaned_transcripts = "\n".join(transcripts).strip()
            return cleaned_transcripts
        raise ValueError("Unable to find segments on show page.")
    raise ValueError("Non 200 status code returned.")
