---
title: Data Analyst Agent with OpenAI Assistants
emoji: 📊
colorFrom: orange
colorTo: red
sdk: gradio
python_version: '3.11'
app_file: app.py
pinned: false
---

# 🤖 Data Analyst Agent with OpenAI Assistants

This project demonstrates a powerful data analysis agent built using the official **OpenAI Assistants API**. The agent leverages the built-in **Code Interpreter** tool to analyze user-uploaded CSV files, answer questions, and generate visualizations.

The web interface is created with Gradio, and the project environment is managed by `uv`.

## 🚀 How to Use the Live Demo

1.  **Upload a CSV File:** Use the file uploader to select a `.csv` file from your computer.
2.  **Ask a Question:** In the textbox, ask a question about your data in plain English. For example:
    * "What is the average age in the dataset?"
    * "Create a pie chart showing the distribution of categories."
    * "What are the key insights from this data? Provide one recommendation."
3.  **Run Analysis:** Click the "Run Analysis" button. The agent will process your file and question on OpenAI's servers and return a detailed text answer along with any generated plots.

---

## 🛠️ Local Setup and Execution (For Developers)

Follow these steps to run the application on your own machine.

### 1. Clone the Repository

```bash
git clone [https://github.com/Shiverion/Data-analysis-using-OpenAI-Assistant.git](https://github.com/Shiverion/Data-analysis-using-OpenAI-Assistant.git)
cd your-repo-name
```
2. Set Up the Environment with uv
This project uses uv for fast and reproducible environment management.

First, install uv if you haven't already:

# On macOS / Linux
```bash
curl -LsSf [https://astral.sh/uv/install.sh](https://astral.sh/uv/install.sh) | sh
```

# On Windows
``` bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then, sync the environment. This command creates a virtual environment and installs the exact package versions from the uv.lock file.

```bash
uv sync
```

### 3. Set Up Your API Key
Create a file named `.env` in the root of the project and add your OpenAI API key to it:
    OPENAI_API_KEY='your-secret-key-here'

### 4. Run the Application
Use `uv` to run the app within the managed environment:

``` bash
uv run app.py
```
--- 

Open the local URL (e.g., http://127.0.0.1:7860) in your browser.

📄 File Structure
- **app.py:** The main Gradio application script containing the agent logic.

- **requirements.txt:** A list of Python dependencies for Hugging Face Spaces.

- **uv.lock:** A definitive lockfile for reproducible environments with uv.

- **.env:** Local file for storing your secret API key (ignored by Git).

- **.gitignore:** Specifies files for Git to ignore.