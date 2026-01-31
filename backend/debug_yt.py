from youtube_transcript_api import YouTubeTranscriptApi
print(dir(YouTubeTranscriptApi))
try:
    YouTubeTranscriptApi.get_transcript("sPxg3dvnB_k")
    print("SUCCESS")
except Exception as e:
    print(f"FAILED: {e}")
