from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
from fastapi.responses import JSONResponse
import validators
import logo  # Assuming your logo extraction function is in a module named 'logo'
import hq
import vision,mission
from urllib.parse import urlparse

app = FastAPI()

class URLRequest(BaseModel):
    website_url: str

    @validator('website_url')
    def validate_url(cls, v):
        """
        Validate that the input URL has a valid scheme and netloc.

        Args:
            v (str): The URL to validate.

        Raises:
            ValueError: If the URL does not have a valid scheme or netloc.

        Returns:
            str: The validated URL.
        """
        parsed = urlparse(v)
        if not all([parsed.scheme in ('http', 'https'), parsed.netloc]):
            raise ValueError('Invalid URL format')
        return v


@app.post("/url")
async def upload_url(request: URLRequest):
    """
    Handle POST requests to the /url endpoint. Validate the URL and process it using various functions.

    Args:
        request (URLRequest): The request body containing the URL.

    Returns:
        JSONResponse: A response containing the results of the processing functions or error details.
    """
    try:
        # Validate that the input URL is correctly formatted
        validated_url = request.website_url
        
        # Initialize a dictionary to store results
        data = {}
        print("get logo")
        # Fetch the logo URL
        try:
            logo_url = logo.find_logos(validated_url)
            if logo_url.startswith(('http://', 'https://')):
                data["logo"] = logo_url
            else:
                raise HTTPException(status_code=404, detail="No valid logo URL found")
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"Error in logo function: {str(e)}")
        except Exception as e:
            print(f"Error finding logo: {e}")
            data["logo_error"] = "An unexpected error occurred while finding the logo."
        print("get hq")
        # Call the second function
        try:
            result_2 = hq.hq_loc(validated_url)
            data["hq"] = result_2
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"Error in function 2: {str(e)}")
        except Exception as e:
            print(f"Error in function 2: {e}")
            data["hq_error"] = "An unexpected error occurred in function 2."
        print("get vision")
        # Call the third function
        try:
            result_3 = vision.process_urls(validated_url)
            data["vision"] = result_3
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"Error in function 3: {str(e)}")
        except Exception as e:
            print(f"Error in function 3: {e}")
            data["vision_error"] = "An unexpected error occurred in function 3."
        print("get mission")
        # Call the fourth function
        try:
            result_4 = mission.process_urls(validated_url)
            data["mission"] = result_4
        except ValueError as e:
            raise HTTPException(status_code=422, detail=f"Error in function 4: {str(e)}")
        except Exception as e:
            print(f"Error in function 4: {e}")
            data["mission_error"] = "An unexpected error occurred in function 4."

        return JSONResponse(content=data, status_code=200)

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        print(f"Error processing request: {e}")
        return JSONResponse(content={"error": "An unexpected error occurred"}, status_code=500)