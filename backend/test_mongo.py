import asyncio
from app.config import db

async def test():
    await db.client.admin.command("ping")
    print("MongoDB connected successfully")

asyncio.run(test())
