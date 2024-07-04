from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


def distribute(
        obj_to_fill: Union[Donation, CharityProject],
        not_fully_invested: list[Union[Donation, CharityProject]],
        session: AsyncSession,
) -> None:
    for instance in not_fully_invested:
        residual_obj_to_fill = (
            obj_to_fill.full_amount - obj_to_fill.invested_amount
        )
        residual_instance = instance.full_amount - instance.invested_amount

        if residual_obj_to_fill > residual_instance:
            obj_to_fill.invested_amount += residual_instance
            instance = close_process(instance)
            session.add(instance)
        else:
            if residual_obj_to_fill != 0:
                instance.invested_amount += residual_obj_to_fill
                if instance.full_amount == instance.invested_amount:
                    close_process(instance)
                session.add(instance)
            obj_to_fill = close_process(obj_to_fill)
            return


async def distribution_on_create(
        obj_to_fill: Union[Donation, CharityProject],
        session: AsyncSession,
) -> None:
    crud = (charity_project_crud if isinstance(obj_to_fill, Donation)
            else donation_crud)
    not_fully_invested = await crud.get_all_not_fully_invested(session)
    distribute(obj_to_fill, not_fully_invested, session)
    session.add(obj_to_fill)
    await session.commit()
    await session.refresh(obj_to_fill)


def close_process(
        obj: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    obj.invested_amount = obj.full_amount
    obj.fully_invested = True
    obj.close_date = datetime.now()
    return obj
