from pydantic import BaseModel,Field

class TodoCreateSchemas(BaseModel):
    
    title:str=Field(min_length=2,max_length=250)
    description:str=Field(min_length=2,max_length=250)
  
    
class TodoUpdateSchemas(BaseModel):
    title:str |None=None
    description:str |None=None