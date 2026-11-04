from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
import api.db as db

app = FastAPI()

# Pievienojam statisko mapi (CSS failiem) un HTML šablonus (Jinja2)
app.mount("/static", StaticFiles(directory="api/static"), name="static")
templates = Jinja2Templates(directory="api/templates")

# Inicializējam datubāzi (izveido tabulu, ja tās vēl nav)
db.init_db()

# --- DATU MODELIS (Validācija) ---
class ScoreModel(BaseModel):
    # Field(...) nozīmē, ka lauks ir obligāts.
    # min_length un max_length neļauj ievadīt tukšu vai pārāk garu vārdu (Aizsardzība!)
    player: str = Field(..., min_length=1, max_length=20)
    # ge=0 nozīmē "greater or equal" (lielāks vai vienāds ar 0). Neļauj ievadīt negatīvus punktus!
    score: int = Field(..., ge=0)

# --- API ENDPOINTI ---

@app.post("/scores", status_code=status.HTTP_201_CREATED)
def add_score(score_data: ScoreModel):
    """Saņem datus no spēles un ieraksta tos datubāzē.
    Atgriež 201, jo ir izveidots jauns ieraksts."""
    db.insert_score(score_data.player, score_data.score)
    return score_data

# Šo atstājam priekš API (JSON formātā, lai spēle varētu nolasīt)
@app.get("/scores/top")
def get_top_scores():
    """Atgriež JSON formātā 10 labākos rezultātus."""
    return db.get_top_scores()

# --- MĀJASLAPAS (HTML) ---

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    """Atgriež līderu tabulas HTML lapu."""
    scores = db.get_top_scores()
    return templates.TemplateResponse(request=request, name="index.html", context={"scores": scores})

# HTML lapa spēlētāja profilam
@app.get("/players/{name}", response_class=HTMLResponse)
def player_profile(request: Request, name: str):
    """Atgriež spēlētāja profila HTML lapu."""
    stats = db.get_player_stats(name)
    if stats["games_played"] == 0:
        # Ja spēlētājs nav atrasts, atgriež 404 kļūdu
        raise HTTPException(status_code=404, detail="Player not found")
    return templates.TemplateResponse(request=request, name="player.html", context={"name": name, "stats": stats})

# HTML lapa noteikumiem
@app.get("/rules", response_class=HTMLResponse)
def rules_page(request: Request):
    """Atgriež noteikumu HTML lapu."""
    return templates.TemplateResponse(request=request, name="rules.html")

# API statistika (JSON formātā)
@app.get("/players/{name}/stats")
def get_player_stats_api(name: str):
    """Atgriež statistiku JSON formātā (priekš API)."""
    stats = db.get_player_stats(name)
    if stats["games_played"] == 0:
        raise HTTPException(status_code=404, detail="Player not found")
    return stats