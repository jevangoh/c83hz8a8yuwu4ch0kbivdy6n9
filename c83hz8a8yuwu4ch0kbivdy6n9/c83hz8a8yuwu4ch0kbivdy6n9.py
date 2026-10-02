from __future__ import annotations

from typing import Type

from pydantic import model_validator
from httpx import get, post, Response

import skkrfl6asevwuubvfioii3hlm as BaseModel


def c83hz8a8yuwu4ch0kbivdy6n9[Model: BaseModel._](
    model_cls: Type[Model], api_base_url: str = "http://localhost:8000"
) -> Type[Model]:
    class _AutoCreate(model_cls, table=False):  # inherits all SQLModel fields
        @model_validator(mode="after")
        def create(self):
            _if_object_exists_response_: Response = get(
                f"{api_base_url}/{self.__tablename__}/{self.id}"
            )
            if _if_object_exists_response_.status_code == 404:  # object not found, create it
                _payload_ = self.model_dump(mode="json")
                _create_object_response_ = post(
                    f"{api_base_url}/{self.__tablename__}", json=_payload_
                )
                _create_object_response_.raise_for_status()
            return self

    return _AutoCreate
