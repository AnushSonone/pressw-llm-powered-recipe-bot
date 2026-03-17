"""
Pydantic models for the cooking/query API request and response.
"""

from pydantic import BaseModel, Field


class CookingRequest(BaseModel):
    """User message sent to the cooking Q&A endpoint."""

    message: str = Field(..., min_length=1, description="User question or request")
    debug: bool = Field(default=False, description="Include reasoning chain in response")


class CookingResponse(BaseModel):
    """Response: either a refusal or a full answer."""

    refusal: str | None = Field(default=None, description="Set when query is out of scope")
    answer: str | None = Field(default=None, description="Full answer for cooking queries")
    reasoning_chain: list[dict] | None = Field(
        default=None, description="Debug: tool calls and node transitions (when debug=true)"
    )
