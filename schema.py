from pydantic import BaseModel


class BookSchema(BaseModel):
    name: str
    author: str
    release_year: int
