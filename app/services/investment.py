from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Union

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


async def calculate_investment(
        new_investment: Union[CharityProject, Donation],
        session: AsyncSession,
) -> None:
    amount_left = new_investment.full_amount
    if type(new_investment) is Donation:
        active_objs = await charity_project_crud.get_active(session)
    else:
        active_objs = await donation_crud.get_active(session)
    active_objs.sort(key=lambda obj: obj.create_date)

    for active_obj in active_objs:
        amount_to_invest = active_obj.full_amount - active_obj.invested_amount
        if amount_to_invest >= amount_left:
            if amount_to_invest == amount_left:
                close_investment(active_obj)
            else:
                active_obj.invested_amount += amount_left
            close_investment(new_investment)
            break
        else:
            close_investment(active_obj)
            new_investment.invested_amount += amount_to_invest
            amount_left -= amount_to_invest

    await session.commit()
    await session.refresh(new_investment)


def close_investment(investment_obj: Union[CharityProject, Donation]) -> None:
    investment_obj.invested_amount = investment_obj.full_amount
    investment_obj.fully_invested = True
    investment_obj.close_date = datetime.now()
