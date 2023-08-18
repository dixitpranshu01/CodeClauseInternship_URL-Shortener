from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles
import random
import string
import os


app = FastAPI()

# In-memory storage for short-to-long URL mapping
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
    short_url = generate_short_url()
    url_mapping[short_url] = url_item.long_url
    return {"short_url": f"/{short_url}"}

@app.get("/{short_url}")
def redirect_to_original(short_url: str):
    if short_url in url_mapping:
        long_url = url_mapping[short_url]
        return RedirectResponse(url=long_url)  # Redirect to the original long URL
    else:
        raise HTTPException(status_code=404, detail="Short URL not found")

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    return short_url

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
