from pydantic import BaseModel
from typing import List

class Template(BaseModel):
    template_id: int
    account: int
    valid: int
    template_name: str
    to_adr: str
    cc_adr: str
    subject: str

class TemplateList(BaseModel):
    template_list: List[Template]
