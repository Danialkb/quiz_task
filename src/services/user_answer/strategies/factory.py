from abc import ABC, abstractmethod

from enums.question_type import QuestionType
from services.user_answer.strategies.base import AnswerValidationStrategy
from services.user_answer.strategies.fill_gap import FillGapValidation
from services.user_answer.strategies.multi_choice import MultiChoiceValidation
from services.user_answer.strategies.single_choice import SingleChoiceValidation


class IAnswerValidationFactory(ABC):
    @classmethod
    @abstractmethod
    def get_strategy(cls, question_type: QuestionType) -> AnswerValidationStrategy:
        ...


class AnswerValidationFactory(IAnswerValidationFactory):
    strategies: dict[QuestionType, AnswerValidationStrategy] = {
        QuestionType.SINGLE_CHOICE: SingleChoiceValidation(),
        QuestionType.MULTI_CHOICE: MultiChoiceValidation(),
        QuestionType.FILL_GAP: FillGapValidation(),
    }

    @classmethod
    def get_strategy(cls, question_type: QuestionType) -> AnswerValidationStrategy:
        return cls.strategies[question_type]
