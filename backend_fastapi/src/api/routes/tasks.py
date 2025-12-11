from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.core.database import get_db
from src.crud import task as crud_task
from src.schemas import task as task_schema

router = APIRouter()

@router.post("/", response_model=task_schema.Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: task_schema.TaskCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new task.
    """
    return await crud_task.create_task(db=db, task=task_in)

@router.get("/", response_model=List[task_schema.Task])
async def read_tasks(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    """
    Retrieve all tasks.
    """
    tasks = await crud_task.get_tasks(db, skip=skip, limit=limit)
    return tasks

@router.get("/{task_id}", response_model=task_schema.Task)
async def read_task(
    task_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Retrieve a single task by its ID.
    """
    db_task = await crud_task.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.put("/{task_id}", response_model=task_schema.Task)
async def update_task(
    task_id: int, task_in: task_schema.TaskUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update a task.
    """
    db_task = await crud_task.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return await crud_task.update_task(db=db, db_task=db_task, task_in=task_in)

@router.delete("/{task_id}", response_model=task_schema.Task)
async def delete_task(
    task_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Delete a task.
    """
    db_task = await crud_task.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task
