from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.dependencies.language import get_language
from api.dependencies.user import get_user_id
from db.repositories.quiz import QuizRepository
from db.repositories.quiz_session import QuizSessionRepository
from db.repositories.user_answer import UserAnswerRepository
from db.session import get_session
from schemas.quiz_session import (
    QuizSessionCreateSchema,
    QuizSessionCreateResponse,
    QuizSessionResponse,
    QuizSessionFinishedResponse,
)
from services.exceptions.base import ServiceException
from services.exceptions.not_found import NotFoundException
from services.quiz_session.commands.create import CreateQuizSessionCommand
from services.quiz_session.commands.finish import FinishQuizSessionCommand
from services.quiz_session.queries.list import ListQuizSessionsQuery
from services.user_balance.bonus_adder import BonusAdder
from services.user_balance.calculator import QuizBonusCalculator
from services.user_balance.external_api import UserBalanceExternalAPI

router = APIRouter(prefix="/quiz_sessions", tags=["Quiz Sessions V1"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_quiz_session(
    data: QuizSessionCreateSchema,
    user_id: UUID = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
) -> QuizSessionCreateResponse:
    quiz_session_repo = QuizSessionRepository(session)
    quiz_repo = QuizRepository(session)
    use_case = CreateQuizSessionCommand(
        quiz_session_repo=quiz_session_repo, quiz_repo=quiz_repo
    )
    try:
        return await use_case.execute(data, user_id)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@router.get("")
async def get_quiz_sessions(
    user_id: UUID = Depends(get_user_id),
    language: str = Depends(get_language),
    session: AsyncSession = Depends(get_session),
) -> list[QuizSessionResponse]:
    quiz_session_repo = QuizSessionRepository(session)
    use_case = ListQuizSessionsQuery(quiz_session_repo)
    return await use_case.execute(user_id, language)


@router.post("/{session_id}/finish")
async def finish_quiz_session(
    session_id: UUID,
    user_id: UUID = Depends(get_user_id),
    session: AsyncSession = Depends(get_session),
) -> QuizSessionFinishedResponse:
    quiz_session_repo = QuizSessionRepository(session)
    user_answer_repo = UserAnswerRepository(session)
    bonus_calculator = QuizBonusCalculator(user_answer_repo)
    user_balance_api = UserBalanceExternalAPI()
    bonus_adder = BonusAdder(bonus_calculator, user_balance_api)

    use_case = FinishQuizSessionCommand(quiz_session_repo, bonus_adder)
    try:
        return await use_case.execute(session_id, user_id)
    except (NotFoundException, ServiceException) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
