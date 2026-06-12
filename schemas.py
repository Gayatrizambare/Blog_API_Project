from pydantic import BaseModel 

#INPUT SCHEMA
class BlogCreate(BaseModel):
    title : str
    content: str


#output schema
class BlogResponse(BaseModel):
    id : int
    title : str
    content:str

    class config:   #from_attributes = True bridges the gab netween pydantic and sql .It allows Pydantic to automatically read blog.title without crashing.
        from_attributes = True

