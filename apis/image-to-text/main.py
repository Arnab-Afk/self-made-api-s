from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import pytesseract
import io

app = FastAPI()

# CORS ALLOWED
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def extract_text_from_image(image):
    
    image = image.convert("L")
   
    text = pytesseract.image_to_string(image)
    return text

@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    try:
       
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        extracted_text = extract_text_from_image(image)

        return JSONResponse(content={"text": extracted_text}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
