from slugify import slugify
from typing import List
from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from models import PasteRequestModel, PasteResponseModel, Paste

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


def get_paste(slug: str) -> Paste:
    try:
        paste: Paste = Paste.get(Paste.slug == slug)
        return paste
    except Paste.DoesNotExist:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Paste not found.")


def create_paste(paste: PasteRequestModel) -> Paste:
    if not paste.text or not paste.slug:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Bad request.")
    if not paste.title:
        paste.title = paste.text[:30]
    paste_obj = Paste.create(
        slug=slugify(paste.slug),
        title=paste.title,
        text=paste.text,
        signature=paste.signature,
    )
    return paste_obj


@app.get("/{slug}")
async def index(slug: str) -> PasteResponseModel:
    paste = get_paste(slug)
    paste_data = {
        "slug": paste.slug,
        "title": paste.title,
        "text": paste.text,
        "created_at": paste.created_at,
        "signature": paste.signature,
    }

    return PasteResponseModel(**paste_data)

@app.post("/", status_code=HTTP_201_CREATED)
async def create(paste: PasteRequestModel) -> PasteResponseModel:
    paste_obj = create_paste(paste)
    return PasteResponseModel(
        slug=slugify(paste_obj.slug),
        title=paste_obj.title,
        text=paste_obj.text,
        created_at=paste_obj.created_at,
        signature=paste_obj.signature,
    )
