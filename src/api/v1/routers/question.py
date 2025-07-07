from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies.language import get_language
from api.dependencies.user import get_user_id
from db.repositories.question import QuestionRepository
from db.session import get_session
from schemas.question import QuestionResponse
from services.question.queries.list import ListQuestionsByQuizQuery

router = APIRouter(tags=["Questions V1"])


@router.get("/quizzes/{quiz_id}/questions")
async def get_questions_by_quiz(
    quiz_id: UUID,
    language: str = Depends(get_language),
    user_id: UUID = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
) -> list[QuestionResponse]:
    question_repo = QuestionRepository(session)
    use_case = ListQuestionsByQuizQuery(question_repo)

    return await use_case.execute(quiz_id, language, user_id=user_id)
