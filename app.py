"""
FastAPI Portfolio Application
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn
from database import init_db, get_skills, get_projects, add_visitor, save_message

# Create App
app = FastAPI(title="Rubina Bibi - Portfolio", version="1.0.0")

# Mount Static
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Startup
@app.on_event("startup")
async def start():
    init_db()
    print("🚀 Server Started!")

# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    skills = get_skills()
    projects = get_projects()
    
    ip = request.client.host if request.client else "localhost"
    ua = request.headers.get("user-agent", "Unknown")
    add_visitor(ip, ua)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "skills": skills,
        "projects": projects,
        "name": "Rubina Bibi",
        "role": "Aspiring Fullstack Developer | Computer Operator",
        "email": "rubinabibi.khr.tech1144@gmail.com",
        "linkedin": "https://www.linkedin.com/in/rubina-bibi-b87578359",
        "github": "https://github.com/Rubina-Bibi",
        "facebook": "https://www.facebook.com/share/1CJQfwRh4c/"
    })

# API: Skills
@app.get("/api/skills")
async def api_skills():
    skills = get_skills()
    return JSONResponse({"success": True, "data": [{"name": s[0], "category": s[1], "level": s[2]} for s in skills]})

# API: Projects
@app.get("/api/projects")
async def api_projects():
    projects = get_projects()
    return JSONResponse({"success": True, "data": [{"name": p[0], "desc": p[1], "url": p[2]} for p in projects]})

# API: Contact
@app.post("/api/contact")
async def contact(request: Request):
    data = await request.json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    message = data.get("message", "").strip()
    
    if name and email and message:
        save_message(name, email, message)
        return JSONResponse({"success": True, "message": "Message sent! ✅"})
    return JSONResponse({"success": False, "message": "Fill all fields!"}, status=400)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)