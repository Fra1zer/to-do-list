from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from typing import Annotated
from db.db import get_db
from models.tasks import Task
from schemas.tasks import CreateTask


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get('/')
async def get_all_tasks(db: Annotated[AsyncSession, Depends(get_db)]):
    tasks = await db.scalars(select(Task))
    return tasks.all()


@router.post('/')
async def create_task(db: Annotated[AsyncSession, Depends(get_db)], task: CreateTask):
    await db.execute(insert(Task).values(name = task.name,
                                   description = task.description,
                                   status = task.status))
    await db.commit()
    return {'status_code': 201}


@router.put('/')
async def update_task():
    pass


@router.delete('/')
async def delete_task():
    pass
