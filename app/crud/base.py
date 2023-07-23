from pydantic import BaseModel
from typing import Generic, List, Optional, Type, TypeVar
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_all(
            self,
            session: AsyncSession,
    ) -> List[ModelType]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: CreateSchemaType,
            session: AsyncSession,
            user: Optional[User] = None,
    ) -> ModelType:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_active(
            self,
            session: AsyncSession,
    ) -> List[ModelType]:
        db_objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested.is_(False)
            )
        )
        return db_objs.scalars().all()
  