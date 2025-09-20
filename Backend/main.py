# backend/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import hashlib, cv2, numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import io

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:8501"] for Streamlit
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/verify")
async def verify_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image_stream = io.BytesIO(contents)
        image = Image.open(image_stream)
        if image.mode == "RGBA":
            image = image.convert("RGB")

        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        reasons = []
        status = "Verified"

        # 1. QR code check
        decoded_objects = decode(image)
        if not decoded_objects:
            status = "Flagged"
            reasons.append("No QR code found.")
        else:
            reasons.append(f"QR found: {decoded_objects[0].data.decode('utf-8')}")

        # 2. Signature check
        h, w = gray_image.shape
        signature_roi = gray_image[int(h*0.8):h-20, int(w*0.6):w-20]
        if cv2.countNonZero(cv2.adaptiveThreshold(signature_roi,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY_INV,11,2)) < 100:
            status = "Flagged"
            reasons.append("Signature missing.")
        else:
            reasons.append("Signature present.")

        # 3. Logo check
        logo_template = cv2.imread("logo_template.png", 0)
        if logo_template is None:
            raise FileNotFoundError("logo_template.png missing")
        res = cv2.matchTemplate(gray_image, logo_template, cv2.TM_CCOEFF_NORMED)
        if np.amax(res) < 0.8:
            status = "Rejected"
            reasons.append("Logo not found.")
        else:
            reasons.append("Logo detected.")

        # Hash
        doc_hash = hashlib.sha256(contents).hexdigest()

        return {"status": status, "reasons": reasons, "hash": doc_hash}

    except Exception as e:
        return {"status": "Error", "reasons": [str(e)], "hash": None}
