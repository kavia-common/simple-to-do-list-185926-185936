from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models.task import Task
from src.schemas.task import TaskCreate, TaskUpdate
from typing import List, Optional

async def get_task(db: AsyncSession, task_id: int) -> Optional[Task]:
    result = await db.execute(select(Task).filter(Task.id == task_id))
    return result.scalars().first()

async def get_tasks(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Task]:
    result = await db.execute(select(Task).offset(skip).limit(limit))
    return result.scalars().all()

async def create_task(db: AsyncSession, task: TaskCreate) -> Task:
    db_task = Task(**task.model_dump())
    db.add(db_task)
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def update_task(db: AsyncSession, db_task: Task, task_in: TaskUpdate) -> Task:
    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    await db.commit()
    await db.refresh(db_task)
    return db_task

async def delete_task(db: AsyncSession, task_id: int):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    db_task = result.scalars().first()
    if db_task:
        await db.delete(db_task)
        await db.commit()
    return db_task
