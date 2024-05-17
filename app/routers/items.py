from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/{item_id}")
async def read_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "name": items_db[item_id]}

@router.post("/")
async def create_item(item: dict):
    item_id = max(items_db.keys()) + 1
    items_db[item_id] = item['name']
    return {"item_id": item_id, "name": item['name']}

# Пример простого хранилища данных
items_db = {
    1: "Item 1",
    2: "Item 2"
}
