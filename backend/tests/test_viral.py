from app.graph.graph import build_graph
from app.config import config
import time

def test_viral_flow():
    graph = build_graph()
    
    print("🚀 Testing Viral Flow...")
    
    inputs = {
        "topic": "AI Agents",
        "urls": [
            "https://www.youtube.com/watch?v=M_2iU2Nlqv4" # Example semantic kernel ID
        ],
        "tone": "Funny",
        "style": "Viral Thread",
        "platform": "Twitter",
        "num_posts": 2,
        "clean_contents": [],
        "ranked_contents": None,
        "final_posts": [],
        "llm_provider": "openai",
        "llm_api_key": config.get_api_key("openai")
    }

    print(f"Inputs: {inputs}")
    
    try:
        result = graph.invoke(inputs)
        print("\n✅ Execution Successful!")
        print("-" * 50)
        print(f"Number of posts: {len(result['final_posts'])}")
        print("-" * 50)
        for i, post in enumerate(result['final_posts']):
            print(f"POST {i+1}:")
            print(post)
            print("-" * 20)
        print("-" * 50)
    except Exception as e:
        print(f"❌ Execution Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_viral_flow()
