from typing import List
from uuid import uuid4, UUID
import uvicorn
from fastapi import FastAPI, HTTPException, Request

# model
from models import User, Gender, Role, UserUpdateRequest

# prometheus for monitoring
import http.server
import prometheus_client as prom

import logging

app = FastAPI()

db: List[User] = [
    User(id=uuid4(), first_name="Rahul", last_name="Chauhan", gender=Gender.male, roles=[Role.student]),
    User(id=uuid4(), first_name="Ayush", last_name="Chauhan", gender=Gender.female, roles=[Role.admin, Role.user])

]

# Create and configure logger
logging.basicConfig(filename="logs/fastapi.log",
                    format='%(asctime)s %(message)s')

                    # filemode='wa'

# Creating an object
logger = logging.getLogger()
 
# Setting the threshold of logger to DEBUG
logger.setLevel(logging.INFO)

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logs= f" {request.client.host} {request.url.port} {request.url.path} "
    logger.info(logs)
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/api/v1/users")
async def fetch_all_users():
    return db;

@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    return HTTPException(
        status_code=404,
        detail=f"User with id: {user_id} does not exists"
    )

@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f"user with id: {user_id} does not exists"
    )

# logger.debug(db)

if __name__ == "__main__":
    prom.start_http_server(8086)
    uvicorn.run(app, host="0.0.0.0", port=8085)

