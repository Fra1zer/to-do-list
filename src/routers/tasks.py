from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from typing import Annotated
from db.db import get_db
from models import *
from schemas.tasks import CreateTask


router = APIRouter(prefix='/tasks', tags=['tasks'])


@router.get('/{user_name}')
async def get_all_tasks(user_name: str, db: Annotated[AsyncSession, Depends(get_db)]):
    db_user = await db.scalar(select(User.id).where(User.name == user_name))
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    tasks = await db.scalars(select(Task).where(User.id == db_user))
    return tasks.all()


@router.post('/{user_name}')
async def create_task(user_name: str, db: Annotated[AsyncSession, Depends(get_db)], task: CreateTask):
    db_user = await db.scalar(select(User.id).where(User.name == user_name))
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    await db.execute(insert(Task).values(name = task.name,
                                   description = task.description,
                                   status = task.status,
                                   user_id = db_user))
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
