from pydantic import BaseModel

class CreateSessionRequest(BaseModel):
    session_name: str
    admin_name: str

class JoinSessionRequest(BaseModel):
    code: str
    name: str