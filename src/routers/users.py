from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete
from typing import Annotated
from db.db import get_db
from models import *
from schemas.users import CreateUser


router = APIRouter(prefix='/users', tags=['users'])


@router.post('/')
async def create_user(user: CreateUser, db: Annotated[AsyncSession, Depends(get_db)]):
    await db.execute(insert(User).values(name = user.name))
    await db.commit()
    return {'status_code': 201, 'transaction': 'Successful'}


@router.delete('/{user_name}')
async def delete_user(user_name: str, db: Annotated[AsyncSession, Depends(get_db)]):
    db_user = await db.scalar(select(User.id).where(User.name == user_name))
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    await db.execute(delete(User).where(User.id == db_user))
    await db.commit()
    return {'status_code': 200, 'transaction': 'Successful'}
