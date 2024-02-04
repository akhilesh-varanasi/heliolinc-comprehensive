import uvicorn
from fastapi import FastAPI
from routes import model
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:8080", "https://epyc.astro.washington.edu"]

app = FastAPI()
basepath = "/api"
app.include_router(model.router, prefix=basepath)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    
    uvicorn.run(
        "__init__:app",
        host="0.0.0.0",
        port=8332,
        reload=True,
    )