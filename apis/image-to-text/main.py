from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO
import pytesseract

app = FastAPI()

@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Read the image file
        image = Image.open(BytesIO(await file.read()))

        # Perform OCR using Tesseract with custom configurations
        custom_config = r'--oem 3 --psm 6'  # Adjust as needed
        text = pytesseract.image_to_string(image, lang='eng', config=custom_config)

        return JSONResponse(content={"text": text}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
