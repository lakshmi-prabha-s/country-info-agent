import sys
from src.agent import agent_app

def main():
    print("🌍 Country Q&A Agent CLI")
    print("Type 'quit' or 'exit' to stop.\n")
    
    while True:
        try:
            query = input("Ask a question about a country: ").strip()
            if query.lower() in ['quit', 'exit']:
                break
            if not query:
                continue
                
            # Initialize empty state with query
            initial_state = {
                "query": query,
                "country": None,
                "requested_fields": [],
                "api_response": None,
                "final_answer": "",
                "error": None
            }
            
            result = agent_app.invoke(initial_state)
            print(f"\n🤖 Agent: {result['final_answer']}\n")
            print("-" * 40)
            
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit(0)
        except Exception as e:
            print(f"\n[!] An error occurred: {e}\n")

if __name__ == "__main__":
    main()