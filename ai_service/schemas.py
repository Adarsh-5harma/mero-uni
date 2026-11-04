from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal

class ResourceMetadata(BaseModel):
    model_config = ConfigDict(extra = "forbid")

    resource_type: Literal[
        "Notes",
        "Question Banks",
        "Lab Sloutions",
        "Assignments",
        "Past Papers",
        "Syllabus"
    ] = Field(description="The type of the document.")

    semester: int = Field(
        ge=1, le=8, 
        description="Nepali university semester number, must be integer 1-8"
    )
    
    subject: str = Field(
        description="The subject name (e.g., Object Oriented Programming, Data Structures)"
    )
    
    key_topics: List[str] = Field(
        description="A list of 3-5 core technical topics covered in the document"
    )
    
    summary: str = Field(
        description="A brief 2-sentence summary of the document's contents."
    )