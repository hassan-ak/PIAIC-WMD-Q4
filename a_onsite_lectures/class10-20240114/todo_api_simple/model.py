from pydantic import BaseModel

class TODOBase(BaseModel):
    title: str
    description: str

class TODOResponse(TODOBase):
    id: int