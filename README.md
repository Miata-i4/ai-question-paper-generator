# AI-Based Academic Question Paper Generator

This project is a solution for **Problem Statement 03**: *Build a system that generates question papers from syllabus topics according to difficulty levels, question types, and mark distributions.*

## Project Overview

Creating well-balanced, comprehensive academic question papers manually is highly time-consuming for educators. This project leverages **Generative AI** to instantly design professional exam papers. 

Unlike traditional predictive ML models that require massive historical datasets, this project uses Large Language Models (LLMs) to synthesize novel, high-quality academic questions on-demand based on strict constraints (Total Marks, Syllabus Topics, Difficulty).

### Features
* **Customizable Syllabus:** Target specific modules or topics for the exam.
* **Difficulty Scaling:** Generate Easy, Medium, Hard, or Mixed difficulty papers.
* **Format Control:** Automatically structure the paper into Multiple Choice, Short Answer, or Essay sections.
* **Mark Distribution:** The AI ensures the sum of all questions equals the requested Total Marks.
* **Export Ready:** Generates clean Markdown that can be copied directly into Word or PDF.

## Project Structure
* `app.py`: The main Gradio web application and Gemini API integration logic.
* `requirements.txt`: Python dependencies.
* `.env.example`: Template for API key configuration.

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API Key:**
   - Create a file named `.env` in this directory.
   - Add your Google Gemini API key:
     ```
     GEMINI_API_KEY=your_actual_api_key_here
     ```
   *(You can get a free API key from Google AI Studio).*

3. **Run the Application:**
   ```bash
   python app.py
   ```
   Open the provided local URL (usually `http://127.0.0.1:7860`) in your browser to interact with the generator.

## Screenshots
<img width="1920" height="4088" alt="image" src="https://github.com/user-attachments/assets/a155dd27-99d3-451a-b306-9967d5fc7428" />

<img width="1920" height="3538" alt="image" src="https://github.com/user-attachments/assets/ff7da52a-54ce-47d3-8db5-3494ad3d2888" />

<img width="1920" height="3973" alt="image" src="https://github.com/user-attachments/assets/59b5dc44-faaa-4832-a620-0692ead20415" />

<img width="1920" height="3285" alt="image" src="https://github.com/user-attachments/assets/8f9f5867-a802-4a9e-95b4-23e9e28a0de9" />




