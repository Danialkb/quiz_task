from fastapi import Header, HTTPException, status
from uuid import UUID


def get_user_id(x_user_id: UUID = Header()) -> UUID:
    return x_user_id
