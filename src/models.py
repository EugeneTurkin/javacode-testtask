from __future__ import annotations

import typing
import uuid

from fastapi import HTTPException
from sqlalchemy import Integer, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import UUID

from src.database import Base
from src.enums import OperationType
from src.schemas import Operation as OperationSchema, OperationData as OperationDataSchema


class Wallet(Base):
    """ORM model for 'wallets' table."""

    __tablename__ = "wallets"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)

    balance: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)

    async def _deposit(self, session: AsyncSession, amount: int) -> Wallet:
        """Deposit specified amount to a wallet."""
        query = update(Wallet).where(Wallet.id == self.id).values(balance=self.balance + amount).returning(Wallet)
        row = (await session.execute(query)).one()

        return typing.cast(Wallet, row.Wallet)

    async def _withdraw(self, session: AsyncSession, amount: int) -> Wallet:
        """Withdraw specified amount from a wallet."""
        query = update(Wallet).where(Wallet.id == self.id).values(balance=self.balance - amount).returning(Wallet)
        row = (await session.execute(query)).one()

        return typing.cast(Wallet, row.Wallet)

    async def perform_operation(self, session: AsyncSession, operation: OperationDataSchema) -> OperationSchema:
        """Perform an operation on a wallet."""
        if operation.type == OperationType.DEPOSIT:
            updated_wallet = await self._deposit(session=session, amount=operation.amount)
        elif operation.type == OperationType.WITHDRAW:
            updated_wallet = await self._withdraw(session=session, amount=operation.amount)

        return OperationSchema.model_validate(
            {
                "amount": operation.amount,
                "type": operation.type,
                "wallet": updated_wallet,
            },
            from_attributes=True,
        )

    @classmethod
    async def create(cls, session: AsyncSession) -> Wallet:
        """Create a new wallet object."""
        wallet = Wallet()
        session.add(wallet)
        await session.flush()
        return wallet

    @classmethod
    async def get(cls, session: AsyncSession, wallet_uuid: uuid.UUID) -> Wallet:
        """Return a wallet object if it exists or raise a HTTP exception."""
        query = select(Wallet).where(Wallet.id == wallet_uuid)
        row = (await session.execute(query)).one_or_none()
        if row is None:
            raise HTTPException(status_code=404, detail="Resource not found.")
        return typing.cast(Wallet, row.Wallet)
