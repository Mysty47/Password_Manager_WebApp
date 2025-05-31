from pydantic import BaseModel

class PasswordEntry(BaseModel):
    name: str
    password: str 