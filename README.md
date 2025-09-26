Quotes Generator App

I wanted to learn how to build and deploy a small app that could generate and serve motivational quotes (both **AI-generated** and **famous**).  
This project started as a way to practice my self-study in software development and AI integration — and it grew into a **full-stack mini app** I can run locally or deploy to the cloud.

---

##  Features

- **AI Quotes** – generates original motivational quotes using the OpenAI API  
- **Famous Quotes** – randomly selects a curated quote from `famous_quotes.json` with attribution  
- **Hashtags Toggle** – optional hashtags for Twitter/X optimization  
- **CSV Logging** – saves generated quotes into `data/out.csv` for tracking  
- **Web UI** – a clean front-end (`index.html`) served by FastAPI  
  - Theme dropdown + custom input  
  - Character counter (turns red if >280 chars)  
  - Copy-to-clipboard button  
  - Save-to-CSV toggle  
- **API Endpoints** – accessible for integration or automation:
  - `GET /quote/original`
  - `GET /quote/famous`

---

##  Tech Stack

- **Python** (FastAPI, Uvicorn)  
- **OpenAI API** (AI quote generation)  
- **HTML/CSS/JS** (front-end interface)  
- **dotenv** (API key management)  
- **Git + GitHub** (version control, portfolio repo)  

---

##  Project Structure

  quotes-app/ # Project Folder
      
  app.py  # FastAPI server

  quotes_app.py  # Quote generation + logic

  famous_quotes.json  # Curated quotes
   
  requirements.txt  # Dependencies

  .env  # API key (not committed)

   static/
   index.html  # Front-end UI

   data/
   out.csv  # Generated log (auto-created)



   Running Locally

1. Clone the repo
git clone https://github.com/<your-username>/<repo-name>.git
cd quotes-app


2. Create a virtual environment
python -m venv .venv


3. Activate it
Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
Mac/Linux:
source .venv/bin/activate


4. Install dependencies
pip install -r requirements.txt


5. Add your OpenAI API key
Create a file named .env with:
OPENAI_API_KEY=sk-...your-key...


6. Run the server
uvicorn app:app --reload

7. Open in your browser
UI: http://127.0.0.1:8000/

API: http://127.0.0.1:8000/quote/original


   
   Deployment
   
This app can be deployed to free hosting platforms (like Render):

   1-Push this repo to GitHub.

   2-Connect Render to your repo.

   3-Add your OPENAI_API_KEY in Render’s environment variables.

   4-Deploy — and you’ll get a public URL like:
        https://quotes-api.onrender.com


## Data Folder
This project writes generated quotes to `data/out.csv` at runtime.

- The `data/` folder is included in the repo (via a `.gitkeep` file).
- CSV logs themselves are **ignored** by Git to keep the repo clean.
- If you clone this repo, make sure a `data/` folder exists at the project root so the app can save logs.



## Screenshots

**Main UI**
![Main UI](screenshots/ui.png)

**Character Counter Warning**
![Character Counter](screenshots/counter.png)

**Copy-to-Clipboard**
![Copy Button](screenshots/copy.png)

**CSV Log File**
![CSV Log](screenshots/csv.png)

**API Endpoint**
![API](screenshots/api.png)

**Deployed App (Render)**
![Deployed](screenshots/deployed.png)
