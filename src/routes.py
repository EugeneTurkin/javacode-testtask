from __future__ import annotations

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from src import controllers
from src.database import get_session
from src.schemas import Operation as OperationSchema, OperationData as OperationDataSchema, Wallet as WalletSchema


router = APIRouter(tags=["api"])

@router.post(
    "/api/v1/wallets",
    description="Create a wallet object in database.",
    responses={
        status.HTTP_201_CREATED: {"description": "A new wallet has been created."},
    },
    response_model=WalletSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_wallet(
    session: AsyncSession = Depends(get_session),
) -> WalletSchema:
    return await controllers.create_wallet(session)


@router.get(
    "/api/v1/wallets/{wallet_uuid}",
    description="Get a wallet's balance.",
    responses={
        status.HTTP_200_OK: {"description": "Wallet's balance returned."},
        status.HTTP_404_NOT_FOUND: {"description": "Requested resource doesn't exist."},
    },
    response_model=WalletSchema,
    status_code=status.HTTP_200_OK,
)
async def get_balance(
    wallet_uuid: Annotated[UUID, Path(example='366b12d1-b3d8-49f9-8f3d-910aef33e0bb')],
    session: AsyncSession = Depends(get_session),
) -> WalletSchema:
    return await controllers.get_balance(session, wallet_uuid=wallet_uuid)


@router.post(
    "/api/v1/wallets/{wallet_uuid}/operation",
    description="Perform withdraw/deposit operation on a wallet.",
    responses={
        status.HTTP_200_OK: {"description": "Operation's data returned."},
        status.HTTP_404_NOT_FOUND: {"description": "Requested resource doesn't exist."},
    },
    response_model=OperationSchema,
    status_code=status.HTTP_200_OK,
)
async def perform_operation(
    operation: Annotated[OperationDataSchema, Body()],
    wallet_uuid: Annotated[UUID, Path(example='366b12d1-b3d8-49f9-8f3d-910aef33e0bb')],
    session: AsyncSession = Depends(get_session),
) -> OperationSchema:
    return await controllers.perform_operation(operation=operation, session=session, wallet_uuid=wallet_uuid)
