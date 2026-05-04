from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    total_price: float

app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    if item.tax:
        item.total_price = item.price + item.tax
    else:
        item.total_price = item.price
    
    return item

@app.post("/items/add_item/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    
    if item.tax is not None:
        item.total_price = item.price + item.tax
        item_dict.update({"total_price_with_tax": item.total_price})
    
    return item_dict

# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item):
#     return {"item_id": item_id, **item.model_dump()}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    
    if q:
        result.update({"q": q})
    return result