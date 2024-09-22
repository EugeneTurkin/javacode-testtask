from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, Field

from src.enums import OperationType


class Wallet(BaseModel):
    """Wallet schema."""

    id: UUID

    balance: int


class OperationData(BaseModel):
    """Operation's data schema."""

    amount: int
    type: OperationType = Field(..., examples=[OperationType.DEPOSIT, OperationType.WITHDRAW])


class Operation(OperationData):
    """Schema for a wallet's operation."""

    wallet: Wallet
