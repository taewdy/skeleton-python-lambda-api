from dataclasses import dataclass
from typing import Optional
from ..api.exceptions import ValidationError


@dataclass
class Photo:
    album_id: int
    id: int
    title: str
    url: str
    thumbnail_url: str

    @classmethod
    def from_dict(cls, data: dict) -> "Photo":
        """
        Create a Photo instance from a dictionary.
        
        Args:
            data: Dictionary containing photo data
            
        Returns:
            Photo: A new Photo instance
            
        Raises:
            ValidationError: If required fields are missing or invalid
        """
        try:
            return cls(
                album_id=data["albumId"],
                id=data["id"],
                title=data["title"],
                url=data["url"],
                thumbnail_url=data["thumbnailUrl"],
            )
        except KeyError as e:
            raise ValidationError(
                f"Missing required field: {str(e)}",
                {"field": str(e).strip("'")}
            )
        except (TypeError, ValueError) as e:
            raise ValidationError(
                "Invalid data format",
                {"error": str(e)}
            ) 