# Simple LLM Web Interface

A small learning project that connects a plain HTML and JavaScript frontend to Google's Gemini API through a FastAPI backend.

The goal is to practice the full request-and-response flow: sending a question from the browser, calling an LLM on the server, and displaying the answer. The interface is intentionally minimal.

## What it does

- Sends questions to Gemini through a local API.
- Includes previous conversation turns as context for follow-up questions.
- Saves conversation history in the browser's `localStorage`.
- Displays the latest assistant response.

## Built with

- **Python and FastAPI** for the backend.
- **LangChain's Google Generative AI integration** for model calls.
- **HTML and vanilla JavaScript** for the frontend.
- **python-dotenv** for loading the API key from a local `.env` file.

## How it works

1. The browser sends the question and saved conversation history to `POST /ask`.
2. The backend adds the question to the history and joins the turns into one text prompt.
3. Gemini generates a response.
4. The backend returns the response and updated history.
5. The browser displays the answer and saves the history for the next request.

The API key stays on the backend. Conversation history is stored in the browser and sent to the backend and Gemini with each question; there is no database.

## Run locally

You will need Python (3.11 is a suggested starting version for the pinned dependencies) and a [Google AI Studio API key](https://aistudio.google.com/apikey) with access to an available Gemini text model.

### 1. Clone the repository

```bash
git clone https://github.com/NimLordia/Simple-LLM-Web-Interface.git
cd Simple-LLM-Web-Interface
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

If your system uses `python3` instead of `python`, use that command when creating the environment.

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure Gemini

Create a file named `.env` in the repository root, next to `main.py`:

```dotenv
GOOGLE_API_KEY=your_google_api_key_here
```

Keep this file private and do not commit it to Git.

**Model compatibility:** The original code uses `gemini-2.0-flash`. Google lists June 1, 2026 as its shutdown date in the [Gemini model deprecation schedule](https://ai.google.dev/gemini-api/docs/deprecations#gemini-2.0-models). Before running the project, replace that model name in `main.py` with a currently supported text model available to your API key. The dependencies are pinned to the versions used by the original project and may also need updating for newer models.

### 4. Start the backend

From the repository root, with the virtual environment active:

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The API runs at [http://127.0.0.1:8000](http://127.0.0.1:8000). FastAPI's interactive API documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 5. Start the frontend

Open a second terminal in the repository root and activate the virtual environment there too. Then run:

```bash
python -m http.server 5500 --bind 127.0.0.1 --directory frontend
```

Open [http://127.0.0.1:5500](http://127.0.0.1:5500), type a question, and click **Ask**. Keep both terminal processes running and wait for each answer before submitting another question.

## API example

Send this JSON body to `POST /ask`, or try it through `/docs`:

```json
{
  "userInput": "What is an API?",
  "conversationHistory": []
}
```

An illustrative response:

```json
{
  "response": "An API lets software applications communicate with each other.",
  "conversationHistory": [
    "User: What is an API?",
    "Assistant: An API lets software applications communicate with each other."
  ]
}
```

Actual answers vary. For follow-up requests, pass the returned `conversationHistory` back to the API. The frontend handles this automatically.

## Project structure

```text
Simple-LLM-Web-Interface/
|-- main.py               # FastAPI routes and Gemini integration
|-- requirements.txt      # Pinned Python dependencies
|-- README.md
`-- frontend/
    `-- index.html        # Question form, API requests, and local history
```

## Learning scope

This project focuses on connecting a frontend, a Python API, and an LLM. It is intended for local experimentation. Styling, input validation, error handling, and deployment support are basic, and it does not include authentication or automated tests.

The page shows only the latest answer. Previous turns remain in local storage and are used as context even after a refresh, but the page does not display a full transcript. To start over, open the browser's developer console on the frontend page and run:

```javascript
localStorage.removeItem("conversationHistory");
location.reload();
```

The frontend expects the backend at `http://127.0.0.1:8000/ask`. If you change the backend address or port, update the `fetch` URL in `frontend/index.html`.
