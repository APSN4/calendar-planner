from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/{user_id}")
async def read_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user_id, "name": users_db[user_id]}

@router.post("/")
async def create_user(user: dict):
    user_id = max(users_db.keys()) + 1
    users_db[user_id] = user['name']
    return {"user_id": user_id, "name": user['name']}

# Пример простого хранилища данных
users_db = {
    1: "User 1",
    2: "User 2"
}
