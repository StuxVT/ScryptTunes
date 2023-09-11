from pydantic import BaseModel


class SongBlacklist(BaseModel):
    blacklist: list = []
