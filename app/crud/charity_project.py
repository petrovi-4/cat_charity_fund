from datetime import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate, CharityProjectUpdate
)


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
]):

    async def get(
            self,
            project_id: int,
            session: AsyncSession,
    ) -> Optional[CharityProject]:
        charity_project = await session.execute(
            select(CharityProject).where(
                CharityProject.id == project_id
            )
        )
        return charity_project.scalars().first()

    async def update(
            self,
            db_charity_project: CharityProject,
            charity_project_in: CharityProjectUpdate,
            session: AsyncSession,
    ) -> CharityProject:
        charity_project_data = jsonable_encoder(db_charity_project)
        update_data = charity_project_in.dict(exclude_unset=True)

        for field in charity_project_data:
            if field in update_data:
                setattr(db_charity_project, field, update_data[field])
        if db_charity_project.invested_amount == db_charity_project.full_amount:
            db_charity_project.fully_invested = True
            db_charity_project.close_date = datetime.now()

        session.add(db_charity_project)
        await session.commit()
        await session.refresh(db_charity_project)
        return db_charity_project

    async def remove(
            self,
            db_charity_project: CharityProject,
            session: AsyncSession,
    ) -> CharityProject:
        await session.delete(db_charity_project)
        await session.commit()
        return db_charity_project

    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        charity_project = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return charity_project.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)