from fastapi import APIRouter

from api.v1.routers import quiz, question, health, quiz_session, user_answer

router = APIRouter(prefix="/api/v1")

router.include_router(health.router)
router.include_router(quiz.router)
router.include_router(question.router)
router.include_router(quiz_session.router)
router.include_router(user_answer.router)
