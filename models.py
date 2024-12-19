from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ContainerStatus(str, Enum):
    NONE = "None"
    PENDING = "Pending"
    PROCESSING = "Processing"
    SUCCESS = "Success"
    ERROR = "Error"
    CANCEL = "Cancel"
    TIMEOUT = "Timeout"

class Command(BaseModel):
    username: Optional[str] = Field(default=None, alias="username")
    user_message: Optional[str] = Field(default=None, alias="user_message")
    message: str = Field(default="", alias="message")

class CommandsContainer(BaseModel):
    commands: List[Command] = Field(..., alias="commands")
    id: str = Field(..., alias="container_id")
    status: ContainerStatus = Field(..., alias="status")
    is_completed: bool = Field(..., alias="completed")

    class Config:
        allow_population_by_field_name = True