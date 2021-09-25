from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from fastapi.middleware.gzip import GZipMiddleware
import random

from backend.db.database import get_session, create_db_and_tables
from backend.api.base_apis import api_router




app = FastAPI()

app.add_middleware(GZipMiddleware, minimum_size=1000)

app.mount("/front", StaticFiles(directory="frontend/public", html=True), name="front")
app.mount("/build", StaticFiles(directory="frontend/public/build"), name="build")

@app.get('/')
async def front():
   return RedirectResponse(url='front')

@app.get("/rand")
async def hello():
   return random.randint(0, 100)
   

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.on_event("shutdown")
async def shutdown():
   pass
    #await database.disconnect()

app.include_router(api_router, prefix="/api")
