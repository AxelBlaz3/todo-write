from fastapi.routing import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.results import InsertOneResult
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from ..dependencies import get_mongo_client

from ..models.todo import Todo


router = APIRouter()

# Endpoint for creating a todo.
@router.post("/todo")
async def create_todo(todo: Todo, client: AsyncIOMotorClient = Depends(get_mongo_client)):
    # Insert the todo from request body todo.
    todo_insert_result: InsertOneResult = await client.tododb.todos.insert_one(jsonable_encoder(todo))

    # Find the inserted todo with inserted id.
    todo = await client.tododb.todos.find_one({'_id': todo_insert_result.inserted_id})

    # Respond it back to the client.
    return todo
