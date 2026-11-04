# SsnakEe 

Snake spēle, kas izstrādāta ar **Python** un **Pygame**. Tā ietver 1P un 2P lokālo režīmu, divas unikālas mehānikas (Magnēts un Astes nomešana) un tiešsaistes līderu tabulu, kas izmanto **FastAPI** serveri un **SQLite** datubāzi.

##  Kā palaist

Atver divus termināļus ar aktivizētu virtuālo vidi (`.venv`).

**1. Terminālis (Serveris):** Palaid no projekta saknes mapes:
```powershell
uvicorn api.main:app --reload

**game** 

py -m main.client

vai python -m main.client

