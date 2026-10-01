from typing import Literal, Optional, Union

from litellm.caching.caching import DualCache
from litellm.integrations.custom_guardrail import CustomGuardrail
from litellm.proxy._types import UserAPIKeyAuth

BLOCKED_CONTENT_TYPES = ("file", "document")
IMAGE_CONTENT_TYPES = ("image_url", "image")
IMAGE_MODEL = "claude-haiku-4-5-20251001"


class NoFileInputGuardrail(CustomGuardrail):
    async def async_pre_call_hook(
        self,
        user_api_key_dict: UserAPIKeyAuth,
        cache: DualCache,
        data: dict,
        call_type: Literal[
            "completion",
            "text_completion",
            "embeddings",
            "image_generation",
            "moderation",
            "audio_transcription",
            "pass_through_endpoint",
            "rerank",
        ],
    ) -> Optional[Union[Exception, str, dict]]:
        has_image = False
        for msg in data.get("messages", []):
            content = msg.get("content", "")
            if isinstance(content, list):
                for part in content:
                    content_type = part.get("type", "")
                    if content_type in BLOCKED_CONTENT_TYPES:
                        raise Exception(
                            "Files and documents inputs are not allowed. "
                            "Please extract text from these files and send them as text."
                        )
                    if content_type in IMAGE_CONTENT_TYPES:
                        has_image = True

        # if has_image:
        #     data["model"] = IMAGE_MODEL

        return data
