from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
    CharityProjectDB,
)
from app.crud.charity_project import charity_project_crud
from app.api.validators import (
    check_name_duplicate,
    check_project_exists,
    check_closed_project,
    check_invested_amount,
    check_before_change_full_amount,
)
from app.services.distribution import distribution_on_create

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    summary='Get all projects.',
    description='Возвращает список всех проектов.',
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session=session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Create project.',
    description='Только для суперюзеров.'
                'Создаёт благотворительный проект.',
)
async def create_new_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    await distribution_on_create(obj_to_fill=new_project, session=session)
    return new_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Update project.',
    description='Только для суперюзеров.'
                'Закрытый проект нельзя редактировать; '
                'нельзя установить требуемую сумму '
                'меньше уже вложенной.',
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    await check_closed_project(project_id, session)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_before_change_full_amount(
            amount_in=obj_in.full_amount,
            project_id=project_id,
            session=session,
        )
    return await charity_project_crud.update(
        project,
        obj_in,
        session,
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    summary='Delete project.',
    description='Только для суперюзеров.'
                'Удаляет проект. Нельзя удалить проект, '
                'в который уже были инвестированы средства, '
                'его можно только закрыть.',
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)
    await check_invested_amount(project_id=project_id, session=session)
    return await charity_project_crud.remove(project, session)
