from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.post("/register")
async def register_user():
    return {"msg": "register endpoint"}

@auth_router.post("/login")
async def login_user():
    return {"msg": "login endpoint"}
