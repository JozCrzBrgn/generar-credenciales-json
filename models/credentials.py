
from pydantic import BaseModel
from typing import List

class CredencialesInput(BaseModel):
    names: List[str]
    usernames: List[str]
    passwords: List[str]