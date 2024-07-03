from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.core.constants import INVESTED_START_AMOUNT


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name,
        session,
    )
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_closed_project(
        project_id: int,
        session: AsyncSession,
) -> None:
    project = await charity_project_crud.get(project_id, session)
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_invested_amount(
        project_id: int,
        session: AsyncSession,
) -> None:
    project = await charity_project_crud.get(obj_id=project_id,
                                             session=session)
    if project.invested_amount > INVESTED_START_AMOUNT:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_before_change_full_amount(
        project_id: int,
        session: AsyncSession,
        amount_in: int,
) -> None:
    project = await charity_project_crud.get(obj_id=project_id,
                                             session=session)
    if amount_in < project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=('''Нелья установить значение full_amount
                    меньше уже вложенной суммы.''')
        )
