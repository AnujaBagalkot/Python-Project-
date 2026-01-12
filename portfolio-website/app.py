from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sys
sys.path.append('..')
from utils.ad_gen import generate_ads
from utils.location import analyze_location

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/ad-generator", response_class=HTMLResponse)
async def ad_generator_page(request: Request):
    return templates.TemplateResponse("ad_generator.html", {"request": request})


@app.post("/generate-ads")
async def generate_ads_api(
    business: str = Form(...),
    location: str = Form(...),
    audience: str = Form(...)
):
    result = generate_ads(business, location, audience)
    return {"ads": result}


@app.get("/location-intel", response_class=HTMLResponse)
async def location_intel_page(request: Request):
    return templates.TemplateResponse("location_intel.html", {"request": request})


@app.post("/analyze-location")
async def analyze_location_api(
    location: str = Form(...),
    business_type: str = Form(...)
):
    result = analyze_location(location, business_type)
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)