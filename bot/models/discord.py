from typing import List, Optional
import requests
from pydantic import BaseModel, Field, HttpUrl

from .webhook_url import WEBHOOK_URL


class Author(BaseModel):
    name: str

class Field_(BaseModel):
    name: str
    value: str
    inline: Optional[bool] = False


class Thumbnail(BaseModel):
    url: HttpUrl


class Image(BaseModel):
    url: HttpUrl


class Footer(BaseModel):
    text: str
    icon_url: Optional[HttpUrl] = None


class AllowedMentions(BaseModel):
    parse: Optional[List[str]] = Field(
        default=[],
        description="Can include 'roles', 'users', and 'everyone'"
    )
    roles: Optional[List[str]] = None
    users: Optional[List[str]] = None


class Embed(BaseModel):
    author: Optional[Author] = None
    title: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None
    color: Optional[int] = None


class DiscordWebhook(BaseModel):
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    content: Optional[str] = Field(None, max_length=2000)
    embeds: Optional[List[Embed]] = None
    tts: Optional[bool] = False

    class Config:
        model_config = {
            "json_schema_extra": {
                "example": {
                    "username": "Webhook",
                    "avatar_url": "https://i.imgur.com/4M34hi2.png",
                    "content": "Text message. Up to 2000 characters.",
                    "embeds": [{
                        "author": {
                            "name": "Birdie♫",
                            "url": "https://www.reddit.com/r/cats/",
                            "icon_url": "https://i.imgur.com/R66g1Pe.jpg"
                        },
                        "title": "Title",
                        "description": "Text message with *Markdown*",
                        "color": 15258703,
                        "fields": [
                            {
                                "name": "Field 1",
                                "value": "Value 1",
                                "inline": True
                            }
                        ]
                    }]
                }
            }
        }

    def post_message(self) -> requests.Response:
        """
        Send the webhook message to Discord.

        Returns:
            requests.Response: The response from Discord's API

        Raises:
            requests.RequestException: If the request fails
        """
        payload = self.model_dump()

        # Remove None values to keep payload clean
        payload = {k: v for k, v in payload.items() if v is not None}

        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.post(
            WEBHOOK_URL,
            json=payload,
            headers=headers
        )

        response.raise_for_status()
        return response

    @classmethod
    def send_message(
            cls,
            content: str,
            username: Optional[str] = None,
            avatar_url: Optional[str] = None,
            embeds: Optional[List[Embed]] = None
    ) -> requests.Response:
        """
        Convenience method to quickly send a message without creating a webhook instance first.

        Args:
            content: The message content
            username: Optional username override
            avatar_url: Optional avatar URL override
            embeds: Optional list of embeds

        Returns:
            requests.Response: The response from Discord's API
        """
        webhook = cls(
            content=content,
            username=username,
            avatar_url=avatar_url,
            embeds=embeds
        )
        return webhook.post_message()