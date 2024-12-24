# -------------------------------------------------------------------------------- #
# Helper Functions
# -------------------------------------------------------------------------------- #

# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in
import os
import re
import json
from typing import Dict, Any

# Third-party
from youtube_transcript_api import YouTubeTranscriptApi
from pydantic import BaseModel, ValidationError

# Local
from src.utils.logger import logger

# Environment Variables
from dotenv import load_dotenv

load_dotenv()


def get_proxy_dict() -> Dict[str, str]:
    """
    Get the proxy URL.
    """
    PROXY_USERNAME = os.getenv("PROXY_USERNAME")
    PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")
    # TODO: This is using a rotating proxy.
    proxy_url = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@gate.smartproxy.com:7000"
    return {
        "http": proxy_url,
        "https": proxy_url
    }


# -------------------------------------------------------------------------------- #
#  Parse Request Body
# -------------------------------------------------------------------------------- #

def parse_request_body(event: Dict[str, Any], request_model: BaseModel) -> Dict[str, Any]:
    """
    Parse and validate the JSON body from an AWS Lambda event.
    """
    try:
        # 1. Attempt to parse the JSON body.
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError as e:
        logger.error("Failed to decode request body as JSON", exc_info=True)
        raise ValueError("Invalid JSON in request body.") from e

    # 2. Check for empty body.
    if not body:
        logger.error("Received an empty request body.")
        raise ValueError("Request body cannot be empty.")

    # 3. For debugging, log minimal details if needed.
    logger.debug("Parsed JSON body: %s", body)

    # 4. Validate required keys (optional step, but often recommended).
    required_keys = request_model.model_json_schema()["required"]
    missing_keys = [key for key in required_keys if key not in body]

    # 5. If missing keys, raise an error.
    if missing_keys:
        logger.error(f"Missing required keys in body: {missing_keys}. Raising ValueError.")
        raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

    # 5. Return the valid, parsed body.
    return body

# -------------------------------------------------------------------------------- #
# Validate Request Body
# -------------------------------------------------------------------------------- #


def validate_request_body(body: Dict[str, Any], request_model: BaseModel) -> None:
    """
    Validate the request body against the request model.
    """
    try:
        request_model(**body)
        logger.debug(f"Request validation passed for the request model: {request_model}")
    except ValidationError as e:
        logger.error(f"Request validation failed for the request model: {request_model}. Error: {e}. Raising ValueError.")
        raise ValueError(f"Request validation failed. {e} for the request model: {request_model}")


# -------------------------------------------------------------------------------- #
# Extract Video ID from YouTube URL
# -------------------------------------------------------------------------------- #

def get_video_id(youtube_url):
    """
    Extract video ID from a YouTube URL.

    Args:
        youtube_url (str): URL of the YouTube video

    Returns:
        str: The video ID extracted from the URL

    Raises:
        ValueError: If the URL is invalid or video ID cannot be extracted
    """
    # Extract the video ID from the YouTube URL
    video_id_match = re.search(r'(?<=v=)[^&#]+|(?<=be/)[^&#]+', youtube_url)
    if video_id_match:
        logger.debug(f"Extracted video ID from YouTube URL: {video_id_match.group(0)}")
        return video_id_match.group(0)
    else:
        logger.error("Invalid YouTube URL. Please provide a valid link. Raising error.")
        raise ValueError("Invalid YouTube URL. Please provide a valid link.")


def get_youtube_transcript(video_url: str) -> str:
    """
    Fetch and return the transcript of a YouTube video.

    Args:
        video_url (str): URL of the YouTube video

    Returns:
        str: Full transcript text of the video, or error message if failed
    """
    try:
        # Get video ID from the URL
        video_id = get_video_id(video_url)

        # Fetch the transcript using YouTubeTranscriptApi
        try:
            # transcript = YouTubeTranscriptApi.get_transcript(video_id)

            # Check if proxy is enabled
            proxy_enabled = os.getenv("USE_PROXY", "false").lower() == "true"
            logger.debug(f"Proxy enabled: {proxy_enabled}")

            if proxy_enabled:
                transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=get_proxy_dict())
            else:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
        except Exception as e:
            logger.error(f"Error fetching transcript. One may not be available. {str(e)}. Raising error.")
            raise ValueError("Error fetching transcript. One may not be available.")

        # Concatenate all the text parts into a single string
        full_transcript = " ".join([entry['text'] for entry in transcript])
        return full_transcript

    except Exception as e:
        logger.error(f"An unknown error occurred: {str(e)}. Raising error.")
        raise ValueError("An unknown error occurred. Please try again.")
