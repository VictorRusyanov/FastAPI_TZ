from sqlalchemy import select, delete, update

from database import new_session, MemeORM
from schemas import MemeAdd

class MemeRepository:
    @classmethod
    async def add_one(cls, data: MemeAdd):
        async with new_session() as session:
            meme_dict = data.model_dump()
            meme = MemeORM(**meme_dict)
            session.add(meme)
            await session.flush()
            await session.commit()
            return meme.id

    @classmethod
    async def find_all(cls, limit: int, offset: int):
        async with new_session() as session:
            query = select(MemeORM).limit(limit).offset(offset)
            result = await session.execute(query)
            memes = result.scalars().all()
            return memes

    @classmethod
    async def find_by_id(cls, meme_id: int):
        async with new_session() as session:
            query = select(MemeORM).filter(MemeORM.id == meme_id)
            result = await session.execute(query)
            meme = result.scalars().first()
            if not meme:
                return None
            return meme

    @classmethod
    async def delete_by_id(cls, meme_id: int):
        async with new_session() as session:
            query = delete(MemeORM).where(MemeORM.id == meme_id)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def update_meme(cls, meme_id: int, new_name: str):
        async with new_session() as session:
            query = update(MemeORM).where(MemeORM.id == meme_id).values(name=new_name)
            await session.execute(query)
            await session.commit()
