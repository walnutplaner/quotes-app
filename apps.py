from fastapi import FastAPI, Query
from fastapi.responses import PlainTextResponse
from quotes_app import make_original, make_famous, load_famous_quotes

app = FastAPI(title="Quotes API")

FAMOUS = load_famous_quotes("famous_quotes.json")

@app.get("/", response_class=PlainTextResponse)
def home():
    return "OK. Try /quote/original or /quote/famous"

@app.get("/quote/original", response_class=PlainTextResponse)
def quote_original(
    theme: str = Query("discipline and consistent action"),
    tags: bool = Query(True)
):
    return make_original(theme, add_tags=tags)

@app.get("/quote/famous", response_class=PlainTextResponse)
def quote_famous(
    tags: bool = Query(True)
):
    return make_famous(FAMOUS, add_tags=tags)
