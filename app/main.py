from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import user, auth, masterdata
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management System API",
    version="1.0.0",
    description="API for managing employee data, user authentication, and roles in an organization.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins="*",  # Allows listed origins
    allow_credentials=True,  # Allows cookies/Authorization headers
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)
app.include_router(masterdata.router, prefix="/master", tags=["Master Data"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
