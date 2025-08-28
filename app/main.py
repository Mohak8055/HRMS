from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import user, auth, masterdata, userprofile, leave, leave_mail, employee_mail
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management System API",
    version="1.0.0",
    description="API for managing employee data, user authentication, and roles in an organization.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(masterdata.router, prefix="/master", tags=["Master Data"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(userprofile.router, prefix="/userprofile", tags=["User Profile"])
app.include_router(leave_mail.router, prefix="/leave-mail", tags=["Leave Mail"])
app.include_router(employee_mail.router, prefix="/employee-mail", tags=["Employee Mail"])
app.include_router(leave.router, prefix="/leave", tags=["Leave"])


app.mount(
    "/profile-photos",
    StaticFiles(directory="uploads/profile_photos"),
    name="profile-photos"
)