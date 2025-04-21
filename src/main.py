import asyncio

from fastapi import FastAPI
from routers import tasks
from db.db import create_tables


app = FastAPI()
app.include_router(tasks.router)


async def main():
    await create_tables()


if __name__ == '__main__':
    from uvicorn import run
    run("main:app", reload = True)
    asyncio.run(main())
