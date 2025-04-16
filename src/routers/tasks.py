from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
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
    return {'status_code': 201, 'transaction': 'Successful'}


@router.put('/')
async def update_task(db: Annotated[AsyncSession, Depends(get_db)], update_task: CreateTask):
    tasks = await db.scalar(select(Task).where(Task.name == update_task.name))
    if tasks is None:
        raise HTTPException(status_code=404, detail='There is no task found')

    await db.execute(update(Task).where(Task.name == update_task.name).values(
        name = update_task.name,
        description = update_task.description,
        status = update_task.status
    ))
    await db.commit()
    return {'status_code': 200, 'transaction': 'Task update is successful'}


@router.delete('/{id_task}')
async def delete_task(db: Annotated[AsyncSession, Depends(get_db)], id_task: int):
    tasks = await db.scalar(select(Task).where(Task.id == id_task))
    if tasks is None:
        raise HTTPException(status_code=404, detail='There is no task found')

    await db.execute(delete(Task).where(Task.id == id_task))
    await db.commit()
    return {'status_code': 200, 'transaction': 'Task delete is successful'}
