# -------------------------------------------------------------------------------- #
# Imports
# -------------------------------------------------------------------------------- #

# Built-in
import os

# Logger
from src.utils.logger import logger

# Types
from src.utils.types import HandlerApiRequest, BaseApiBody, LambdaApiResponse

# Helpers
from src.utils.helpers import get_youtube_transcript, parse_request_body, validate_request_body



# -------------------------------------------------------------------------------- #
# Handler
# -------------------------------------------------------------------------------- #


def youtube_transcript_handler(event, context):

    logger.info(f"Beginning to fetch YouTube transcript")

    try:
        # Parse Request Body
        parsed_request = parse_request_body(event, HandlerApiRequest)

        # Validate Request Body
        validate_request_body(body=parsed_request, request_model=HandlerApiRequest)

        # Create HandlerApiRequest
        handler_api_request = HandlerApiRequest(**parsed_request)

        # Fetch the transcript
        try:
            transcript = get_youtube_transcript(handler_api_request.youtube_url)
        except Exception as e:
            logger.error(f"Error fetching transcript from {handler_api_request.youtube_url}. {str(e)}")
            raise ValueError("Error fetching transcript. One may not be available.")

        # Return the transcript
        base_api_body = BaseApiBody(data={"transcript": transcript})
        return LambdaApiResponse(body=base_api_body).model_dump_json()

    except ValueError as e:
        logger.error(f"Error: {str(e)}")
        return LambdaApiResponse(statusCode=400,
                                 body=BaseApiBody(status="error", message=str(e)).model_dump_json())


if __name__ == "__main__":
    import json

    event = {
        "body": json.dumps({
            "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        })
    }

    # Fetch the transcript
    print(youtube_transcript_handler(event, None))
