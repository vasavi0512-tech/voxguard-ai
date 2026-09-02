from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from detector import detect_voice_risk
from ml_detector import predict_voice
from scam_detector import analyze_scam_text

import os
import uuid
import tempfile


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


UPLOAD_FOLDER = os.path.join(
    tempfile.gettempdir(),
    "voxguard_uploads"
)


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


class ScamRequest(BaseModel):

    text: str


@app.get("/")
def home():

    return {

        "message":
            "Welcome to VoxGuard AI",

        "team":
            "ECHOX",

        "status":
            "Backend is running"

    }


@app.post("/upload-audio")
async def upload_audio(
    audio: UploadFile = File(...)
):

    file_extension = os.path.splitext(
        audio.filename
    )[1]


    unique_filename = (
        str(uuid.uuid4()) +
        file_extension
    )


    file_path = os.path.join(
        UPLOAD_FOLDER,
        unique_filename
    )


    contents = await audio.read()


    with open(
        file_path,
        "wb"
    ) as file:

        file.write(contents)


    try:

        ai_result = predict_voice(
            file_path
        )


        risk_result = detect_voice_risk(

            ai_result[
                "ai_generated_probability"
            ]

        )


        return JSONResponse(

            content={

                "message":
                    "Audio analyzed successfully",

                "filename":
                    audio.filename,

                "analysis": {

                    "status":
                        "Audio analyzed"

                },

                "risk_analysis":
                    risk_result,

                "ai_prediction":
                    ai_result

            }

        )


    except Exception as error:

        print(
            "Audio analysis error:",
            error
        )


        return JSONResponse(

            status_code=500,

            content={

                "message":
                    "Audio analysis failed",

                "error":
                    str(error)

            }

        )


    finally:

        if os.path.exists(
            file_path
        ):

            try:

                os.remove(
                    file_path
                )

            except Exception:

                pass


@app.post("/analyze-scam")
def analyze_scam(
    request: ScamRequest
):

    result = analyze_scam_text(
        request.text
    )


    return {

        "message":
            "Scam analysis completed",

        "scam_analysis":
            result

    }