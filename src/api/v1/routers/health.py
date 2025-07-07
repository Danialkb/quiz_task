from fastapi import APIRouter
from starlette import status
from starlette.responses import Response

router = APIRouter(tags=["Health Check"])


@router.get("/health")
async def check_health():
    return Response(status_code=status.HTTP_200_OK)
