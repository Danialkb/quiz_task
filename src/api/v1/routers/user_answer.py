from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.dependencies.user import get_user_id
from db.repositories.question import QuestionRepository
from db.repositories.quiz_session import QuizSessionRepository
from db.repositories.user_answer import UserAnswerRepository
from db.session import get_session
from schemas.user_answer import UserAnswerCreateSchema, UserAnswerCreateResponse
from services.exceptions.base import ServiceException
from services.exceptions.not_found import NotFoundException
from services.quiz_session.update import QuizSessionProgressUpdater
from services.user_answer.commands.submit_answer import SubmitAnswerCommand
from services.user_answer.strategies.factory import AnswerValidationFactory

router = APIRouter(prefix="/user_answers", tags=["User Answers V1"])


@router.post("")
async def submit_user_answer(
    data: UserAnswerCreateSchema,
    user_id: UUID = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
) -> UserAnswerCreateResponse:
    question_repo = QuestionRepository(session)
    quiz_session_repo = QuizSessionRepository(session)
    answer_repo = UserAnswerRepository(session)
    answer_validation_factory = AnswerValidationFactory

    session_progress_updater = QuizSessionProgressUpdater(quiz_session_repo)

    use_case = SubmitAnswerCommand(
        question_repo=question_repo,
        answer_validation_factory=answer_validation_factory,
        quiz_session_updater=session_progress_updater,
        answer_repo=answer_repo,
    )
    try:
        return await use_case.execute(data, user_id)
    except (ServiceException, NotFoundException) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)
