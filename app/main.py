from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import user, auth, masterdata, userprofile
from app.database import Base, engine
from app.api.routes import leave_mail

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
app.include_router(userprofile.router, prefix="/userprofile", tags=["User Profile"])
app.include_router(leave_mail.router, prefix="/leave-mail", tags=["Leave Mail"])

app.mount(
    "/profile-photos",
    StaticFiles(directory="uploads/profile_photos"),   # maps to local folder
    name="profile-photos"
)
