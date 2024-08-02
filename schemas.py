from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее сециальное образование'
    HIGHER = 'Высшее образование'


class Person(BaseModel):
    name: str
    surname: Union[str, list[str]]
    age: Optional[int]
    is_staff: bool = False
    education_level: Optional[EducationLevel]