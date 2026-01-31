try:
    import youtube_transcript_api
    print("SUCCESS: youtube_transcript_api imported")
except ImportError as e:
    print(f"FAILURE: {e}")
