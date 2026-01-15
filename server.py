from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import time
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

app = FastAPI()

# Allow browser HTML to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

HEADERS = {
    "User-Agent": "ProductDataTool/1.0"
}

class TestURL(BaseModel):
    url: str

class Product(BaseModel):
    name: str = ""
    upc: str = ""
    ean: str = ""
    url: str = ""

class RunRequest(BaseModel):
    products: list[Product]

def is_blocked(html: str, status: int):
    text = html.lower()
    if status in [401, 403, 429]:
        return True, f"HTTP {status}"
    if any(k in text for k in ["captcha", "robot", "blocked", "access denied"]):
        return True, "Bot protection detected"
    return False, "OK"

def fetch_page(url):
    start = time.time()
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        blocked, reason = is_blocked(r.text, r.status_code)
        return {
            "status": "Blocked" if blocked else "Unblocked",
            "http": r.status_code,
            "reason": reason,
            "html": "" if blocked else r.text,
            "time": int((time.time() - start) * 1000)
        }
    except Exception as e:
        return {
            "status": "Blocked",
            "http": None,
            "reason": str(e),
            "html": "",
            "time": int((time.time() - start) * 1000)
        }

def extract_text(html):
    soup = BeautifulSoup(html, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return soup.get_text(" ", strip=True)

def derive_item_form(text):
    text = text.lower()
    if "capsule" in text: return "Capsule"
    if "tablet" in text: return "Tablet"
    if "powder" in text: return "Powder"
    if "liquid" in text: return "Liquid"
    if "gummy" in text: return "Gummy"
    return ""

def derive_quantity(text):
    m = re.search(r"(\\d+)\\s*(capsules|tablets|servings|softgels)", text.lower())
    return f"{m.group(1)} {m.group(2)}" if m else ""

@app.post("/api/test-url")
def test_url(req: TestURL):
    result = fetch_page(req.url)
    domain = urlparse(req.url).netloc
    return {
        "domain": domain,
        "status": result["status"],
        "http_status": result["http"],
        "reason": result["reason"],
        "time_ms": result["time"]
    }

@app.post("/api/run")
def run(req: RunRequest):
    output = []
    for p in req.products:
        page = fetch_page(p.url) if p.url else None
        text = extract_text(page["html"]) if page and page["status"] == "Unblocked" else ""

        output.append({
            "Product Name": p.name,
            "UPC": p.upc,
            "EAN": p.ean,
            "Source URL": p.url,
            "Source Status": page["status"] if page else "No URL",
            "Item Form": derive_item_form(text),
            "Quantity": derive_quantity(text),
            "Notes": "Blocked sites skipped safely"
        })

    return {
        "output_rows": output
    }

