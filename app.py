import gradio as gr
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# --- Load Environment Variables and Initialize Client ---
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Configuration ---
ASSISTANT_INSTRUCTIONS = """
You are an expert data analyst. When the user uploads a file and asks a question,
your role is to use your Code Interpreter tool to write and run Python code to answer the question.

- Analyze the data thoroughly.
- If the user asks for a visualization, create it and display it as an image in your response.
- If the user doesn't asks for visualization, just make the analysis or whatever user ask.
- Provide a text explanation of your findings and describe any visualizations you create.
- Use Markdown formatting for all text in your output.This includes headings, bullet points, code blocks (if any), and emphasis for clarity.
"""
PLOT_FILENAME = "assistant_plot.png"

# --- Assistant Logic ---
def analyze_with_assistant(file_obj, user_prompt):
    """
    Orchestrates the OpenAI Assistant to analyze a user-provided file.
    """
    # 1. Input Validation
    if file_obj is None:
        return "Error: Please upload a file first.", None
    if not user_prompt:
        return "Error: Please enter a question.", None

    # Cleanup old plot file
    if os.path.exists(PLOT_FILENAME):
        os.remove(PLOT_FILENAME)

    try:
        # 2. Upload the user's file to OpenAI
        uploaded_file = client.files.create(
            file=open(file_obj.name, "rb"),
            purpose="assistants"
        )

        # 3. Create an Assistant
        # This defines the agent's behavior and tools.
        assistant = client.beta.assistants.create(
            name="Data Analyst Assistant",
            instructions=ASSISTANT_INSTRUCTIONS,
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-turbo",
            tool_resources={"code_interpreter": {"file_ids": [uploaded_file.id]}}
        )

        # 4. Create a Thread (a conversation session)
        thread = client.beta.threads.create()

        # 5. Add the User's Message to the Thread
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_prompt
        )

        # 6. Run the Assistant
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        # 7. Wait for the Run to complete
        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

        if run.status != 'completed':
            return f"Error: The Assistant run failed with status {run.status}", None

        # 8. Retrieve and Process Messages
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_response = ""
        image_file_id = None

        # The latest message is from the assistant
        for content_part in messages.data[0].content:
            if content_part.type == "text":
                assistant_response += content_part.text.value
            elif content_part.type == "image_file":
                image_file_id = content_part.image_file.file_id

        # 9. Download the image if it exists
        image_path = None
        if image_file_id:
            image_data = client.files.content(image_file_id)
            image_data_bytes = image_data.read()
            with open(PLOT_FILENAME, "wb") as f:
                f.write(image_data_bytes)
            image_path = PLOT_FILENAME
        
        return assistant_response, image_path

    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}"
        print(error_message)
        return error_message, None

# --- Gradio UI (Largely unchanged) ---
with gr.Blocks(theme=gr.themes.Soft(primary_hue="orange")) as demo:
    gr.Markdown(
        """
        # 🤖 Agentic Data Analysis with OpenAI Assistants
        This version uses the official OpenAI Assistants API with the Code Interpreter tool.
        """
    )
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload your CSV", file_types=[".csv"])
            text_input = gr.Textbox(
                label="What would you like to know?",
                placeholder="e.g., 'What is the correlation between column A and B?' or 'Create a bar chart of sales by category.'"
            )
            submit_button = gr.Button("🚀 Run Analysis", variant="primary")
        
        with gr.Column(scale=2):
            text_output = gr.Markdown(label="📝 Agent's Answer")
            plot_output = gr.Image(label="📊 Generated Visualization", type="filepath")

    submit_button.click(
        fn=analyze_with_assistant,
        inputs=[file_input, text_input],
        outputs=[text_output, plot_output]
    )

if __name__ == "__main__":
    demo.launch()
