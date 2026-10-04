import gradio as gr
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
# In a real environment, you would ensure GEMINI_API_KEY is set in your .env file
api_key = os.getenv("GEMINI_API_KEY")
if api_key and api_key != "your_api_key_here":
    genai.configure(api_key=api_key)
    MODEL_READY = True
else:
    MODEL_READY = False

def generate_question_paper(subject, topics, difficulty, question_types, total_marks, instructions):
    if not MODEL_READY:
        return "⚠️ Error: Gemini API Key not found. Please add your GEMINI_API_KEY to the .env file."
    
    if not topics.strip():
        return "⚠️ Error: Please provide at least one syllabus topic."

    # Construct the prompt
    prompt = f"""
    You are an expert academic professor. Generate a formal academic question paper based on the following parameters:
    
    - Subject: {subject}
    - Syllabus Topics: {topics}
    - Difficulty Level: {difficulty}
    - Allowed Question Types: {', '.join(question_types)}
    - Total Marks: {total_marks}
    - Additional Instructions: {instructions}
    
    Format the output as a professional exam paper. Include:
    1. A Header (Course Name, Total Marks, Time Allowed: 3 Hours)
    2. General Instructions for the students
    3. Clearly divided sections based on the requested Question Types (e.g., Section A: Multiple Choice, Section B: Short Answer).
    4. Ensure the total marks of all questions exactly adds up to {total_marks}.
    5. Provide a well-structured, easy-to-read markdown format.
    
    Do NOT provide the answers, only the question paper.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during generation: {str(e)}"

# Define the Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📝 AI-Based Academic Question Paper Generator")
    gr.Markdown("Build custom, well-formatted exam papers instantly using Generative AI based on your syllabus topics and constraints.")
    
    if not MODEL_READY:
        gr.Markdown("### ⚠️ Setup Required: Please create a `.env` file with `GEMINI_API_KEY=your_key` and restart the app.")
    
    with gr.Row():
        with gr.Column(scale=1):
            subject_input = gr.Textbox(label="Subject / Course Name", placeholder="e.g. Data Structures and Algorithms")
            topics_input = gr.TextArea(label="Syllabus Topics", placeholder="e.g. Arrays, Linked Lists, Trees, Graph Theory, Sorting Algorithms", lines=4)
            difficulty_input = gr.Radio(choices=["Easy", "Medium", "Hard", "Mixed"], label="Difficulty Level", value="Mixed")
            
            q_types_input = gr.CheckboxGroup(
                choices=["Multiple Choice (1 Mark)", "Short Answer (2 Marks)", "Long Answer / Essay (5-10 Marks)", "Practical / Coding (15 Marks)"],
                label="Question Types",
                value=["Short Answer (2 Marks)", "Long Answer / Essay (5-10 Marks)"]
            )
            
            marks_input = gr.Number(label="Total Marks", value=50, minimum=10, maximum=100)
            instructions_input = gr.Textbox(label="Additional Instructions (Optional)", placeholder="e.g. Include at least 2 real-world scenario questions")
            
            generate_btn = gr.Button("Generate Question Paper 🚀", variant="primary")
            
        with gr.Column(scale=1):
            output_paper = gr.Markdown(label="Generated Question Paper")
            
    generate_btn.click(
        fn=generate_question_paper,
        inputs=[subject_input, topics_input, difficulty_input, q_types_input, marks_input, instructions_input],
        outputs=output_paper
    )

if __name__ == "__main__":
    demo.launch(share=False, theme=gr.themes.Soft())
