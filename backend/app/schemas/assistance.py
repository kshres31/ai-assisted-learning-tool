from typing import Annotated

from pydantic import BaseModel, Field

from app.services.assistance_service import AssistanceReply


class HintRequest(BaseModel):
    code: Annotated[str, Field(max_length=8_000)] = ""
    level: Annotated[int, Field(ge=1, le=3)] = 1


class ExplainRequest(BaseModel):
    code: Annotated[str, Field(max_length=8_000)] = ""


class AssistanceResponse(BaseModel):
    kind: str
    content: str
    provider: str
    level: int | None
    fallback_reason: str | None

    @classmethod
    def from_domain(cls, reply: AssistanceReply) -> "AssistanceResponse":
        return cls(
            kind=reply.kind,
            content=reply.content,
            provider=reply.provider,
            level=reply.level,
            fallback_reason=reply.fallback_reason,
        )
