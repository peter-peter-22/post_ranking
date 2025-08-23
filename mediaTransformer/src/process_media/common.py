from pydantic import BaseModel
from dataclasses import dataclass

class Vector2IntSchema(BaseModel):
    x:int
    y:int

@dataclass
class Vector2Int:
    x:int
    y:int