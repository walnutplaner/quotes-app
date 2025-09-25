from fastapi import FastAPI, Query, Request
from fastapi.responses import PlainTextResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from quotes_app import make_original, make_famous, load_famous_quotes, export_csv

app = FastAPI(title="Quotes API")

# Load famous quotes once (restart server if you edit famous_quotes.json)
FAMOUS = load_famous_quotes("famous_quotes.json")

# --- API endpoints ---
@app.get("/quote/original", response_class=PlainTextResponse)
def quote_original(
    request: Request,
    theme: str = Query("discipline and consistent action"),
    tags: bool = Query(True),
    save: bool = Query(False)
):
    text = make_original(theme, add_tags=tags)
    if save:
        export_csv([{"created_at": "web", "type": "original", "text": text}])
    return text

@app.get("/quote/famous", response_class=PlainTextResponse)
def quote_famous(
    request: Request,
    tags: bool = Query(True),
    save: bool = Query(False)
):
    text = make_famous(FAMOUS, add_tags=tags)
    if save:
        export_csv([{"created_at": "web", "type": "famous", "text": text}])
    return text

# --- Serve the front-end (index.html) ---
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def root():
    return FileResponse("static/index.html")
