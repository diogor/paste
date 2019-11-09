from typing import List
from fastapi import FastAPI, HTTPException
from starlette.status import (HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
                              HTTP_404_NOT_FOUND)
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from models import (PasteRequestModel,
                    PasteResponseModel,
                    Paste)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_paste(id: int) -> Paste:
    try:
        paste: Paste = Paste.get(Paste.id == id)
        return paste
    except Paste.DoesNotExist:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Paste not found.")


def create_paste(paste: PasteRequestModel) -> Paste:
    if not paste.text:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Bad request.")
    if not paste.title:
        paste.title = paste.text[:30]
    paste_obj = Paste.create(
        title=paste.title,
        text=paste.text,
        signature=paste.signature
    )
    return paste_obj


@app.get("/{id}")
async def index(id: int) -> PasteResponseModel:
    paste = get_paste(id)
    paste_data = {
        "id": paste.id,
        "title": paste.title,
        "text": paste.text,
        "created_at": paste.created_at,
        "signature": paste.signature
    }

    return PasteResponseModel(**paste_data)


@app.get("/{id}/related")
async def index(id: int) -> List[PasteResponseModel]:
    paste = get_paste(id)
    pastes: List[PasteResponseModel]

    if paste.signature:
        entries = Paste.select().where(
            Paste.signature == paste.signature,
            Paste.id != paste.id
        ).order_by(Paste.created_at.desc()).dicts()
        pastes = [
            PasteResponseModel(**paste) for
            paste in entries
        ]
        return pastes

    return []


@app.post("/", status_code=HTTP_201_CREATED)
async def create(paste: PasteRequestModel) -> PasteResponseModel:
    paste_obj = create_paste(paste)
    return PasteResponseModel(
        id=paste_obj.id,
        title=paste_obj.title,
        text=paste_obj.text,
        created_at=paste_obj.created_at,
        signature=paste_obj.signature
    )