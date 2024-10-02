from fastapi import FastAPI
import funcaptcha_challenger
import base64
from PIL import Image
import io
import uvicorn
from pydantic import BaseModel



app = FastAPI()


async def process_image(image_data, image_type):
    try:
        decoded_image_data = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(decoded_image_data))
        results = funcaptcha_challenger.predict(image, image_type)
        return results
    except Exception as e:
        print(f"Error processing image: {e}")
        return None


class Data(BaseModel):
    image: str
    type_image: str


@app.get("/")
async def root():
    return {
        "api": {
            "call": "/createTask",
            "post": {
                "image": "image_file base64 encoding",
                "type_image": "type funchaptha"
            }
        }
    }


@app.get('/ping')
async def ping_route():
    return {"message": "Pong"}


@app.post('/createTask')
async def create_task(data: Data):
    prediction_results = await process_image(data.image, data.type_image)
    if prediction_results is None:
        return {"error": True, "result": "An error occurred while processing the image"}
    



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True, workers=4)