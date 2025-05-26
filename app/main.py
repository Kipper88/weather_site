from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .weather import get_forecast
from .database import init_db, save_search, get_search_stats

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="supersecret")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

init_db()

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    last_city = request.session.get("last_city", "")
    return templates.TemplateResponse(request, "index.html", {"request": request, "last_city": last_city})

@app.post("/weather", response_class=HTMLResponse)
async def weather(request: Request, city: str = Form(...)):
    forecast = await get_forecast(city)
    save_search(city)
    request.session["last_city"] = city
    return templates.TemplateResponse(request, "index.html", {"request": request, "forecast": forecast, "city": city})


@app.get("/api/search-stats")
async def stats():
    return JSONResponse(get_search_stats())
