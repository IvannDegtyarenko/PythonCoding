from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class STaskAdd(BaseModel):
    name: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    completed: Optional[bool] = False

class STask(STaskAdd):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)