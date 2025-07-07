from fastapi import Header

from enums.language import Language


def get_language(
    x_language: str = Header(default=None),
) -> str:
    if not x_language or x_language not in Language:
        return Language.ENGLISH.value
    return x_language
