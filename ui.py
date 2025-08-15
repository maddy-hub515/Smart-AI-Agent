import gradio as gr
from memory_store import save_to_memory
from agent import smart_agent
from tts import speak_text_offline

# Store the last result globally to give feedback later
last_result = {"issue": "", "solution": "", "source": ""}

def create_entry(issue, solution, category):
    if not issue or not solution:
        return "❌ Please provide both Issue and Solution."
    save_to_memory(issue, solution, source="User", category=category or "General")
    return "✅ Issue and Solution saved successfully."

def get_solution(query):
    global last_result
    if not query:
        return "❌ Please enter a query.", gr.update(visible=False), gr.update(visible=False)
    
    response = smart_agent(query)
    results = response.get("results",[])

    if results:
        # Just using the first result for feedback (simplification)
        first = results[0]
        if isinstance(first, dict):
            solution = first.get("solution", "No solution found.")
            issue = first.get("issue", "Unknown issue")
            source = response.get("source", "AI")

            # Speak
            speak_text_offline(solution)

            # Save to global
            last_result["issue"] = issue
            last_result["solution"] = solution
            last_result["source"] = source

            # Return solution + make thumbs visible only if AI
            return solution, gr.update(visible=(source == "AI"))

        else:
            return str(first), gr.update(visible=False), gr.update(visible=False)

    return "😕 No matching solution found.", gr.update(visible=False), gr.update(visible=False)

def handle_feedback(value):
    if not last_result["issue"] or not last_result["solution"]:
        return "⚠️ No previous result to give feedback for."
    save_to_memory(
        last_result["issue"],
        last_result["solution"],
        source="AI",
        category="General",
        feedback=value
    )
    return "✅ Thanks for your feedback!"

def feedback_action(value):
    message = handle_feedback(value)
    return "", "", gr.update(visible=False), gr.Info(message)

    
with gr.Blocks(title="Smart AI Agent with Voice") as demo:
    gr.Markdown("## 🤖 Smart AI Agent\nChoose an option below")

    with gr.Tab("📝 Create Issue & Solution"):
        issue_input = gr.Textbox(label="Enter Issue", placeholder="e.g. App crashing when clicking submit")
        solution_input = gr.Textbox(label="Enter Solution", placeholder="e.g. Check if the submit button triggers multiple requests")
        category_input = gr.Textbox(label="Optional: Category", placeholder="e.g. Backend, DevOps")
        create_button = gr.Button("Save Issue")
        create_output = gr.Textbox(label="Status")

        create_button.click(
            fn=create_entry,
            inputs=[issue_input, solution_input, category_input],
            outputs=create_output
        )

    with gr.Tab("🧠 Ask for Solution"):
        query_input = gr.Textbox(label="Describe Your Issue", placeholder="e.g. Submit button doesn't work")
        query_button = gr.Button("Get Solution")
        query_output = gr.Textbox(label="Suggested Solution", lines=6)

        feedback_row = gr.Row(visible=False)
        with feedback_row:
            thumbs_up = gr.Button("👍", size="sm")
            thumbs_down = gr.Button("👎", size="sm")

    query_button.click(
            fn=get_solution,
            inputs=[query_input],
            outputs=[query_output, feedback_row]
        )
    
    # Feedback with clear + hide + popup
    thumbs_up.click(
        fn=lambda: feedback_action("👍"),
        inputs=[],
        outputs=[query_input, query_output, feedback_row]
    )
    thumbs_down.click(
        fn=lambda: feedback_action("👎"),
        inputs=[],
        outputs=[query_input, query_output, feedback_row]
    )
    
demo.launch()