from dataclasses import dataclass
from typing import Optional


@dataclass
class Photo:
    album_id: int
    id: int
    title: str
    url: str
    thumbnail_url: str

    @classmethod
    def from_dict(cls, data: dict) -> "Photo":
        return cls(
            album_id=data["albumId"],
            id=data["id"],
            title=data["title"],
            url=data["url"],
            thumbnail_url=data["thumbnailUrl"],
        ) 