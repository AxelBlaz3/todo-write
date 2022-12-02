from fastapi.routing import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import InsertOneResult
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from ..dependencies import get_mongo_client

from ..models.todo import Todo


router = APIRouter()

@router.post("/todo")
async def create_todo(todo: Todo, client: AsyncIOMotorClient = Depends(get_mongo_client)):
    todo_insert_result: InsertOneResult = await client.tododb.todos.insert_one(jsonable_encoder(todo))
    todo = await client.tododb.todos.find_one({'_id': todo_insert_result.inserted_id})
    return todo
