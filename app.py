import gradio as gr
import google.generativeai as genai
import os
from dotenv import load_dotenv
from duckduckgo_search import DDGS

# Load environment variables
load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key and api_key != "your_api_key_here":
    genai.configure(api_key=api_key)
    MODEL_READY = True
else:
    MODEL_READY = False

def fetch_real_world_context(subject, topics):
    """Searches the web for real exam questions (like NCERT/CBSE) to use as inspiration."""
    query = f"{subject} {topics} NCERT CBSE previous year question paper questions"
    context = ""
    try:
        results = DDGS().text(query, max_results=3)
        for res in results:
            context += f"- {res['body']}\n"
    except Exception as e:
        context = f"(Web search failed: {str(e)})"
    return context

def generate_question_paper(subject, topics, difficulty, question_types, total_marks, instructions):
    if not MODEL_READY:
        return "⚠️ Error: Gemini API Key not found. Please add your GEMINI_API_KEY to the .env file."
    
    if not topics.strip():
        return "⚠️ Error: Please provide at least one syllabus topic."
        
    gr.Info("Searching the web for real-world question inspiration...")
    search_context = fetch_real_world_context(subject, topics)

    # Construct the prompt with strict formatting and math rules
    prompt = rf"""
    You are an expert academic professor and examiner. Generate a formal academic question paper based strictly on the following parameters.
    
    --- PARAMETERS ---
    Subject: {subject}
    Syllabus Topics: {topics}
    Difficulty Level: {difficulty}
    Allowed Question Types: {', '.join(question_types)}
    Target Total Marks: {total_marks}
    Additional Instructions: {instructions}
    
    --- REAL WORLD INSPIRATION ---
    Use the following real-world web search snippets as inspiration for framing high-quality, board-level (e.g. NCERT) questions:
    {search_context}
    
    --- STRICT CONSTRAINTS ---
    1. MATH EXACTNESS: The total marks for all generated questions MUST sum exactly to {total_marks}. Calculate carefully. Do not exceed or fall short of {total_marks}.
    2. SCIENTIFIC SYMBOLS & CHEMICAL REACTIONS (CRITICAL): 
       - You must use proper LaTeX for all chemical formulas, equations, and math.
       - Enclose inline chemical formulas and symbols in single dollar signs (e.g., `$\text{{Fe}}^{{2+}}$`, `$\text{{H}}_2\text{{O}}$`).
       - Enclose full chemical reactions in double dollar signs so they render correctly on their own line. For example:
         $$ \text{{K}}_2\text{{Cr}}_2\text{{O}}_7 + 4\text{{H}}_2\text{{SO}}_4 + 3\text{{H}}_2\text{{S}} \rightarrow \text{{K}}_2\text{{SO}}_4 + \text{{Cr}}_2(\text{{SO}}_4)_3 + 7\text{{H}}_2\text{{O}} + 3\text{{S}} $$
    3. FORMATTING:
       - Header: Course Name, Total Marks: {total_marks}, Time Allowed: 3 Hours
       - General Instructions
       - Clearly divided sections based on the requested Question Types.
       - Clearly indicate the marks for each question at the end of the question (e.g., [2 Marks]).
    
    Do NOT provide the answers, only the question paper. Ensure all scientific symbols are wrapped in $ or $$ for LaTeX rendering.
    """
    
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during generation: {str(e)}"

# Define the Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📝 AI-Based Academic Question Paper Generator (Web-Augmented)")
    gr.Markdown("Build custom, well-formatted exam papers instantly using Generative AI. This app searches the web (NCERT/CBSE) for real-world question inspiration and renders chemical equations perfectly.")
    
    if not MODEL_READY:
        gr.Markdown("### ⚠️ Setup Required: Please create a `.env` file with `GEMINI_API_KEY=your_key` and restart the app.")
    
    with gr.Row():
        with gr.Column(scale=1):
            subject_input = gr.Textbox(label="Subject / Course Name", placeholder="e.g. Chemistry, Data Structures")
            topics_input = gr.TextArea(label="Syllabus Topics", placeholder="e.g. D Block elements, Periodic table trends", lines=3)
            difficulty_input = gr.Radio(choices=["Easy", "Medium", "Hard", "Mixed"], label="Difficulty Level", value="Mixed")
            
            q_types_input = gr.CheckboxGroup(
                choices=["Multiple Choice (1 Mark)", "Short Answer (2 Marks)", "Long Answer / Essay (5 Marks)", "Practical / Complex (10 Marks)"],
                label="Question Types",
                value=["Short Answer (2 Marks)", "Long Answer / Essay (5 Marks)"]
            )
            
            marks_input = gr.Number(label="Total Marks", value=50, minimum=10, maximum=100)
            instructions_input = gr.Textbox(label="Additional Instructions (Optional)", placeholder="e.g. Include at least 2 real-world scenario questions")
            
            generate_btn = gr.Button("Search Web & Generate Question Paper 🚀", variant="primary")
            
        with gr.Column(scale=1):
            output_paper = gr.Markdown(
                label="Generated Question Paper (LaTeX Supported)", 
                latex_delimiters=[
                    {"left": "$$", "right": "$$", "display": True},
                    {"left": "$", "right": "$", "display": False}
                ]
            )
            
    generate_btn.click(
        fn=generate_question_paper,
        inputs=[subject_input, topics_input, difficulty_input, q_types_input, marks_input, instructions_input],
        outputs=output_paper
    )

if __name__ == "__main__":
    demo.launch(share=False, theme=gr.themes.Soft())
