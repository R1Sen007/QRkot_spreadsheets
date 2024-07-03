from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationRegularUserDB


class CRUDDonation(CRUDBase):
    async def get_all_donations_by_user(
            self,
            user_id: int,
            session: AsyncSession,
    ) -> list[DonationRegularUserDB]:
        db_donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user_id
            )
        )
        db_donations = db_donations.scalars().all()
        return db_donations

    async def get_all_not_fully_invested(
            self,
            session: AsyncSession,
    ) -> list[Donation]:
        donations = await session.execute(
            select(Donation).where(
                Donation.fully_invested == False # noqa
            ).order_by(Donation.create_date)
        )
        donations = donations.scalars().all()
        return donations


donation_crud = CRUDDonation(Donation)
