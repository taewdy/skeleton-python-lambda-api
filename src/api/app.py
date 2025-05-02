from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ..clients.http.client import HTTPClient
from ..photos.services import PhotoService
from ..photos.models import Photo

app = FastAPI(
    title="Photos API",
    description="API for retrieving photos from JSONPlaceholder",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
http_client = HTTPClient("https://jsonplaceholder.typicode.com")
photo_service = PhotoService(http_client)


@app.get("/photos", response_model=list[Photo])
async def get_photos():
    """Get a list of photos."""
    return photo_service.get_photos()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 