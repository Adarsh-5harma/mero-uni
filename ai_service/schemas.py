from pydantic import BaseModel, Field, ConfigDict
from typing import List, Literal, Optional # Import Optional

class ResourceMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    resource_type: Literal[
        "notes", 
        "question-bank", 
        "lab-solutions", 
        "assignments", 
        "past-papers", 
        "syllabus"
    ] = Field(description="The type of the document.")
    
    # Change this line:
    semester: Optional[int] = Field(
        default=None,
        ge=1, 
        le=8,
        description="Nepali university semester number (1-8). Return null if not explicitly mentioned in the text."
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