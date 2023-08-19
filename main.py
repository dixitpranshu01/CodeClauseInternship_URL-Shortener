from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
import hashlib
import os

app = FastAPI()

# In-memory storage for long-to-short URL mapping
url_mapping = {}

class URLItem(BaseModel):
    long_url: str

# Mount the "html" folder as a static directory
app.mount("/html", StaticFiles(directory="html"), name="html")

@app.get("/")
def home():
    return FileResponse("html/page.html")

@app.post("/shorten")
def shorten_url(url_item: URLItem):  # Use URLItem model for request body
    short_url = generate_short_url(url_item.long_url)
    url_mapping[url_item.long_url] = short_url
    return {"short_url": f"/{short_url}"}

@app.get("/{short_url}")
def redirect_to_original(short_url: str):
    for long_url, generated_short_url in url_mapping.items():
        if generated_short_url == short_url:
            return RedirectResponse(url=long_url)  # Redirect to the original long URL
    raise HTTPException(status_code=404, detail="Short URL not found")

def generate_short_url(long_url: str):
    hash_object = hashlib.md5(long_url.encode())  # Use MD5 hash
    return hash_object.hexdigest()[:6]  # Use the first 6 characters of the hash

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
