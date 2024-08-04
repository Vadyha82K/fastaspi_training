import re

from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator, root_validator
from fastapi import FastAPI


class EducationLevel(str, Enum):
    SECONDARY = 'Среднее образование'
    SPECIAL = 'Среднее сециальное образование'
    HIGHER = 'Высшее образование'


class Person(BaseModel):
    name: str = Field(
        ..., min_length=2, max_length=20,
        title='Полное имя', description='Можно вводить в любом регистре'
    )
    surname: Union[str, list[str]] = Field(..., min_length=2, max_length=50)
    age: Optional[int] = Field(None, gt=4, le=99)
    is_staff: bool = Field(False, alias='is-staff')
    education_level: Optional[EducationLevel]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    'name': 'Eduardo',
                    'surname': ['Santos', 'Tavares'],
                    'age': 20,
                    'is_staff': False,
                    'education_level': 'Среднее образование'
                }
            ]
        }
    }


    @field_validator('name')
    @classmethod
    def name_cant_be_numeric(cls, value: str):
        if value.isnumeric():
            raise ValueError('Имя не может быть числом')
        return value


    @root_validator(skip_on_failure=True)
    def using_different_languages(cls, values):
        surname = ''.join(values['surname'])
        checked_value = values['name'] + surname
        if (re.search('[а-я]', checked_value, re.IGNORECASE)
                and re.search('[a-z]', checked_value, re.IGNORECASE)):
            raise ValueError('Пожалуйста, не смешивайте русские и латинские буквы')
        return values