from fastapi import FastAPI, Request
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import ebay, oxfam, categories

load_dotenv()

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

#ORIGIN = "https://{}".format(os.environ.get('DOMAIN'))
ORIGIN = "http://localhost:3000"
origins = [
    ORIGIN,
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers =["Access-Control-Allow-Credentials", "Access-Control-Allow-Origin"])
]

app = FastAPI(middleware=middleware)

@app.middleware("http")
async def add_access_origin_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = ORIGIN
    return response


app.include_router(ebay.router)
app.include_router(oxfam.router)
app.include_router(categories.router)