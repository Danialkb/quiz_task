from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.language import get_language
from api.dependencies.user import get_user_id
from db.repositories.quiz import QuizRepository
from db.session import get_session
from schemas.quiz import QuizResponse
from services.exceptions.not_found import NotFoundException
from services.quiz.queries.get_by_id import GetQuizQuery
from services.quiz.queries.list import ListQuizzesQuery

router = APIRouter(prefix="/quizzes", tags=["Quizzes V1"])


@router.get("/")
async def list_quizzes(
    language: str = Depends(get_language),
    user_id: UUID = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
) -> list[QuizResponse]:
    quiz_repo = QuizRepository(session)
    use_case = ListQuizzesQuery(quiz_repo)

    return await use_case.execute(user_id, language)


@router.get("/{quiz_id}")
async def get_quiz(
    quiz_id: UUID,
    language: str = Depends(get_language),
    user_id: UUID = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
) -> QuizResponse:
    quiz_repo = QuizRepository(session)
    use_case = GetQuizQuery(quiz_repo)

    try:
        return await use_case.execute(quiz_id, language, user_id=user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.detail)
