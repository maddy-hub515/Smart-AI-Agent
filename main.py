import os
from memory_store import save_to_memory
from agent import smart_agent

# Load environment variables from .env


def main():
    print("🤖 Smart AI Agent") 
    
    while True:
        print("\nSelect Option:\n1. Create Issue & Solution\n2. Ask for a Solution\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == "3":
            break

        elif choice == "1":
            issue = input("\n📝 Enter the ISSUE:\n")
            solution = input("💡 Enter the SOLUTION:\n")
            category = input("🏷️ Optional - Enter category (or press Enter to skip): ")
            save_to_memory(issue, solution, source="User", category=category or "General")

        elif choice == "2":
            query = input("\n🧠 Describe your issue to get a solution:\n")
            response = smart_agent(query)
            results = response.get("results", [])
            if results:
                for result in results:
                    if isinstance(result, dict):
                        print("\n📌 Issue:", result.get("issue", "N/A"))
                        print("✅ Solution:", result.get("solution", "N/A"))
                        print("📂 Source:", response.get("source", "N/A"))

                        # Ask for feedback only if from AI
                        if response["source"] == "AI":
                            feedback = input("🗳️ Was this helpful? (y/n): ").strip().lower()
                            if feedback == "y":
                                print("✅ Saved to memory with positive feedback.")
                                save_to_memory(result["issue"], result["solution"], source="AI", category="General", feedback="👍")
                            elif feedback == "n":
                                print("❌ Marking feedback as negative.")
                                save_to_memory(result["issue"], result["solution"], source="AI", category="General", feedback="👎")
                    else:
                        print("\n⚠️ Unexpected result format:", result)

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()