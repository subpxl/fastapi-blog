from fastapi import FastAPI
from routers import blog,auth
from fastapi.middleware.cors import CORSMiddleware
from scheduler import start_scheduler, shutdown_scheduler
from database import Base,engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
def on_startup() -> None:
    start_scheduler()

@app.on_event("shutdown")
def on_shutdown()-> None:
    shutdown_scheduler()
    
# @app.get("/")
# async def root():
#     return {"message":"hello from blog"}


app.include_router(blog.router,prefix="/api/blogs",tags=["blogs"])
app.include_router(auth.router,prefix="/api/auth",tags=["auth"])


if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app",port=8000,reload=True)