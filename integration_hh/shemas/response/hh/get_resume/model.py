from typing import Annotated, List

from pydantic import BaseModel, Field

class Contact(BaseModel):
    type: Annotated[str, Field(..., description="Contact type")]
    value: Annotated[str, Field(..., description="Value type")]


class GetResumeModel(BaseModel):
    first_name: Annotated[str, Field(..., description="First name")]
    middle_name: Annotated[str, Field(..., description="Middle name")]
    last_name: Annotated[str, Field(..., description="Last name")]
    contacts: Annotated[List[Contact], Field(..., description="Contact details")]
    ...