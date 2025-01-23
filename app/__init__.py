from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(continent.router, tags=["Continents"])
app.include_router(country.router, tags=['Countries'])


@app.get("/api/fastapi")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}