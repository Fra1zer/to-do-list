import asyncio

from fastapi import FastAPI
from routers import tasks
from routers import users
from db.db import create_tables


app = FastAPI()
app.include_router(tasks.router)
app.include_router(users.router)


async def main():
    await create_tables()


if __name__ == '__main__':
    asyncio.run(main())
