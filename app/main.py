from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request # Add Request here
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.routes import user, auth, masterdata, userprofile, leave, leave_mail, employee_mail, broadcast
from app.database import Base, engine
from app.websocket_manager import manager
import json

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

# HTTP Routers
app.include_router(masterdata.router, prefix="/master", tags=["Master Data"])
app.include_router(user.router, prefix="/user", tags=["User"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(userprofile.router, prefix="/userprofile", tags=["User Profile"])
app.include_router(leave_mail.router, prefix="/leave-mail", tags=["Leave Mail"])
app.include_router(employee_mail.router, prefix="/employee-mail", tags=["Employee Mail"])
app.include_router(leave.router, prefix="/leave", tags=["Leave"])
app.include_router(broadcast.router, prefix="/broadcast", tags=["Broadcast"])

# WebSocket Endpoint for employees
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Internal endpoint for the consumer to post messages to
@app.post("/internal/broadcast")
async def internal_broadcast(request: Request):
    message = await request.json()
    await manager.broadcast(json.dumps(message))
    return {"status": "message broadcasted"}


app.mount(
    "/profile-photos",
    StaticFiles(directory="uploads/profile_photos"),
    name="profile-photos"
)