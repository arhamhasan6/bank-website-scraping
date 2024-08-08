
from fastapi import FastAPI,Body
from typing import List , Dict
from pydantic import BaseModel
import logo
from fastapi.responses import JSONResponse

app = FastAPI()

class URLRequest(BaseModel):
    website_url: str

@app.post("/url")
async def upload_url(request: URLRequest):
    try:
        
            logo_url = logo.get_logo_url(request.website_url)
            print(logo_url)
            data = {"logo": logo_url}
            return JSONResponse(content=data, status_code=202)
                # Alternatively, return JSONResponse(content=json_data, status_code=200)

    except Exception as e:
            print(f"Error finding logo: {e}")
            return JSONResponse({"keywords": []}, status_code=204)
        
