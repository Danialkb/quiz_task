from fastapi import Header, HTTPException, status
from uuid import UUID


def get_user_id(x_user_id: str = Header()) -> UUID:
    try:
        return UUID(x_user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid X-User-ID format",
        )
