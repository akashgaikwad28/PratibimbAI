import youtube_transcript_api
import sys

print(f"Python Version: {sys.version}")
print(f"Module file: {getattr(youtube_transcript_api, '__file__', 'None')}")
print(f"Module dir: {dir(youtube_transcript_api)}")

if hasattr(youtube_transcript_api, 'YouTubeTranscriptApi'):
    cls = youtube_transcript_api.YouTubeTranscriptApi
    print(f"Class type: {type(cls)}")
    print(f"Class dir: {dir(cls)}")
else:
    print("Class YouTubeTranscriptApi NOT FOUND in module")
