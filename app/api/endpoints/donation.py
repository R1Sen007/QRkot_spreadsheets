from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.schemas.donation import (
    DonationCreate,
    DonationRegularUserDB,
    DonationSuperUserDB,
)
from app.crud.donation import donation_crud
from app.models.user import User
from app.services.distribution import distribution_on_create

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationSuperUserDB],
    dependencies=[Depends(current_superuser)],
    summary='Get all donations.',
    description='Только для суперюзеров.'
                'Возвращает список всех пожертвований.',
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_multi(session=session)


@router.post(
    '/',
    response_model=DonationRegularUserDB,
    summary='Create new donation.',
    description='Сделать пожертвование.',
)
async def get_all_donations(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    donation = await donation_crud.create(donation, session, user)
    await distribution_on_create(obj_to_fill=donation, session=session)
    return donation


@router.get(
    '/my',
    response_model=list[DonationRegularUserDB],
    summary='Get only user donation.',
    description='Вернуть список пожертвований пользователя, '
                'выполняющего запрос.',
)
async def get_all_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_all_donations_by_user(user.id, session)
