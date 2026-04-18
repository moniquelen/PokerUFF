import random
import string
import os
from core.session_store import sessions
from fastapi import HTTPException

# Gerar código único para as sessões (no momento da criação)
def generate_code():
    while True:
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if code not in sessions:
            return code

# =======================
# Configurações da sessão
# =======================

def create_session_service(name: str):
    if not name or not name.strip():
        raise HTTPException(status_code=400, detail="Nome obrigatório")
     
    code = generate_code()

    sessions[code] = {
        "name": name,
        "participants": [],
        "votes": {},
        "revealed": False
    }

    return {
        "code": code,
        "name": name
    }

def join_session_service(code: str, name: str):
    if not code or not name or not name.strip():
        raise HTTPException(status_code=400, detail="Dados inválidos")
    
    session = sessions.get(code)

    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    if name not in session["participants"]:
        session["participants"].append(name)
    
    print("Participantes:", session["participants"])
    
    return {"message": "Entrou na sessão"}

def get_session_state(code: str):
    session = sessions.get(code)

    if not session:
        return {
            "participants": [],
            "votes": {},
            "revealed": False
        }

    return {
        "participants": session["participants"],
        "votes": session["votes"],
        "revealed": session["revealed"]
    }

# =======================
# Configuração dos votos
# =======================

def save_vote(code: str, user: str, value: int):
    session = sessions.get(code)

    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    session["votes"][user] = value

    return {"message": "Voto registrado"}


def reveal_votes(code: str):
    session = sessions.get(code)

    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    session["revealed"] = True

    return {"message": "Votos revelados"}


def reset_votes(code: str):
    session = sessions.get(code)

    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")

    session["votes"] = {}
    session["revealed"] = False

    return {"message": "Votação reiniciada"}

print("PROCESS ID:", os.getpid())