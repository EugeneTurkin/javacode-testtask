from __future__ import annotations

from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Wallet
from src.schemas import Operation as OperationSchema, OperationData as OperationDataSchema, Wallet as WalletSchema


async def create_wallet(session: AsyncSession) -> WalletSchema:
    """Create a new wallet."""
    wallet = await Wallet.create(session=session)

    return WalletSchema.model_validate(wallet, from_attributes=True)


async def get_balance(session: AsyncSession, wallet_uuid: UUID) -> WalletSchema:
    """Get a wallet's balance."""
    wallet = await Wallet.get(session, wallet_uuid)

    return WalletSchema.model_validate(wallet, from_attributes=True)


async def perform_operation(session: AsyncSession, wallet_uuid: UUID, operation: OperationDataSchema) -> OperationSchema:
    """Perform an operation on a wallet."""
    wallet = await Wallet.get(session, wallet_uuid)

    operation = await wallet.perform_operation(session, operation)

    return operation
