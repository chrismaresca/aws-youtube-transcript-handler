# -------------------------------------------------------------------------------- #
# Types
# -------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


# -------------------------------------------------------------------------------- #
# API Request Types
# -------------------------------------------------------------------------------- #


class HandlerApiRequest(BaseModel):
    """Request model for the handler API."""
    youtube_url: str = Field(description="The URL of the YouTube video to fetch the transcript from.")

# -------------------------------------------------------------------------------- #
# API Response Types
# -------------------------------------------------------------------------------- #

class BaseApiBody(BaseModel):
    """
    Base model for the API body. Includes status, message, and data.
    """
    status: str = Field(description="The status of the response", default="success")
    message: str = Field(description="The message of the response", default="The request was successful")
    data: Optional[Dict[str, Any]] = Field(description="The response from the AI models", default=None)


# -------------------------------------------------------------------------------- #

class LambdaApiResponse(BaseModel):
    """
    Response model for the Lambda HTTP handler.
    """
    statusCode: int = Field(description="The status code of the response", default=200)
    headers: Dict[str, str] = Field(description="The headers of the response", default={"Content-Type": "application/json"})
    body: BaseApiBody = Field(description="The body of the response. Includes status, message, and data.", default=BaseApiBody())
