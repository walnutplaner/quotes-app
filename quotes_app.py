import json, random, re, csv, os, hashlib, time
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

MAX_LEN = 280
HASHTAG_POOLS = [
    ["#motivation", "#inspiration", "#mindset", "#growth"],
    ["#creativity", "#discipline", "#focus", "#resilience"],
    ["#buildinpublic", "#success", "#habits", "#learn"]
]

def sanitize(s: str) -> str:
    import re
    return re.sub(r"\s+", " ", s).strip()

def fits_tweet(s: str) -> bool:
    return len(s) <= MAX_LEN

def add_hashtags(text: str, n=2) -> str:
    tags = random.sample(random.choice(HASHTAG_POOLS), k=n)
    candidate = f"{text} {' '.join(tags)}"
    return candidate if len(candidate) <= MAX_LEN else text

def dedupe_guard(text: str, seen_hashes: set) -> bool:
    h = hashlib.sha256(text.lower().encode()).hexdigest()[:16]
    if h in seen_hashes:
        return False
    seen_hashes.add(h)
    return True

def load_famous_quotes(path="famous_quotes.json"):
    if not os.path.exists(path): return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    clean = []
    for q in data:
        text = sanitize(q.get("text", ""))
        author = sanitize(q.get("author", ""))
        source = sanitize(q.get("source", "")) if q.get("source") else ""
        if text and author:
            clean.append({"text": text, "author": author, "source": source})
    return clean

def pick_famous(quotes):
    return random.choice(quotes) if quotes else None

def format_famous_quote(q: dict) -> str:
    base = f"“{q['text']}” — {q['author']}"
    if q.get("source"):
        cand = f"{base} ({q['source']})"
        return cand if len(cand) <= MAX_LEN else base
    return base

# ---------- OpenAI LLM ----------
def generate_with_llm(theme: str = "discipline and consistent action") -> str:
    """
    Uses OpenAI Chat Completions to generate one original, short quote.
    """
    load_dotenv()
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Write ONE original motivational quote (max 220 chars).
Voice: grounded, specific; no clichés, no emojis, no hashtags.
Theme: {theme}
Avoid: 'hustle', 'grind', generic platitudes.
Output ONLY the quote line, no author."""
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.8,
        max_tokens=120
    )
    return resp.choices[0].message.content.strip()

def make_original(theme: str, add_tags=True) -> str:
    raw = sanitize(generate_with_llm(theme))
    if len(raw) > 240:
        raw = raw[:237].rstrip() + "..."
    out = add_hashtags(raw, n=2) if add_tags else raw
    return out if len(out) <= MAX_LEN else raw

def make_famous(quotes, add_tags=True) -> str:
    q = pick_famous(quotes)
    if not q: return "Add some quotes to famous_quotes.json first."
    base = format_famous_quote(q)
    out = add_hashtags(base, n=2) if add_tags else base
    return out if len(out) <= MAX_LEN else base

def export_csv(rows, path="data/out.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = ["created_at", "type", "text"]
    new = not os.path.exists(path)
    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if new: w.writeheader()
        for r in rows: w.writerow(r)

# Optional: simple CLI run when called directly
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--theme", default="discipline and consistent action")
    parser.add_argument("--type", choices=["original","famous"], default="original")
    args = parser.parse_args()

    quotes = load_famous_quotes()
    seen = set()
    if args.type == "original":
        txt = make_original(args.theme, add_tags=True)
        if dedupe_guard(txt, seen) and fits_tweet(txt):
            print(txt)
            export_csv([{"created_at": datetime.utcnow().isoformat(), "type":"original", "text": txt}])
    else:
        txt = make_famous(quotes, add_tags=True)
        if dedupe_guard(txt, seen) and fits_tweet(txt):
            print(txt)
            export_csv([{"created_at": datetime.utcnow().isoformat(), "type":"famous", "text": txt}])
