from __future__ import annotations

from json import dumps
from threading import Event as AwaitEvent
from typing import Any, cast, get_origin
from uuid import UUID as Uuid
from uuid import uuid4 as generate_id

import eibzpkxvd6ejecypxs4pqrez3 as ReadableAndWritableDependency
import msjzm0ilrcvjjguhp29y62uzk as the_redis_client
import q6uwngw0268p337x2mz5z8yi3 as the_redis_listening_thread
import skkrfl6asevwuubvfioii3hlm as BaseModel
from httpx import Response, get, patch, post
from pydantic.fields import FieldInfo
from PySide6.QtCore import Qt

type RequestId = Uuid


def c83hz8a8yuwu4ch0kbivdy6n9[Model: BaseModel._](
    model_class: type[Model], default_base_url: str | None
) -> type[Model]:

    class _AutoCreate(model_class, table=False):  # type: ignore[call-arg, valid-type, misc]
        def __init__(self, **data: Any) -> None:
            super().__init__(**data)
            if self.base_url is None:
                return

            the_redis_listening_thread._.register(self.id)
            _object_exists_response_: Response = get(
                f"{self.base_url}/{self.__tablename__}/{self.id}"
            )
            if _object_exists_response_.status_code == 404:
                _create_object_response_ = post(
                    f"{self.base_url}/{self.__tablename__}", json=self.model_dump(mode="json")
                )
                _create_object_response_.raise_for_status()
            the_redis_listening_thread._.active_objects[self.id].updated.connect(
                self.handle_redis_update, Qt.ConnectionType.DirectConnection
            )

        def handle_redis_update(self, request_id: RequestId) -> None:
            _get_object_response_: Response = get(f"{self.base_url}/{self.__tablename__}/{self.id}")
            _get_object_response_.raise_for_status()
            _object_data: dict[str, Any] = _get_object_response_.json()
            for _attribute_name_, _new_value_ in _object_data.items():
                if not hasattr(self, _attribute_name_):
                    continue
                _object_attribute_ = getattr(self, _attribute_name_)
                if isinstance(_object_attribute_, ReadableAndWritableDependency._):
                    _object_attribute_.value = _new_value_
                else:
                    setattr(self, _attribute_name_, _new_value_)
            if request_id in self._active_requests:
                self._active_requests[request_id].set()

        def __setattr__(self, name: str, value: Any) -> None:
            _model_fields_: dict[str, FieldInfo] = type(self).model_fields
            if name in _model_fields_:
                _field_info_: FieldInfo = _model_fields_[name]
                _origin_class_ = get_origin(_field_info_.annotation) or _field_info_.annotation
                if isinstance(_origin_class_, type) and issubclass(
                    _origin_class_, ReadableAndWritableDependency._
                ):
                    if self.base_url is None:
                        _object_attribute_: ReadableAndWritableDependency._ = cast(
                            ReadableAndWritableDependency._, getattr(self, name)
                        )
                        if _object_attribute_.value == value:
                            return
                        _object_attribute_.value = value
                        return

                    _request_id_: RequestId = generate_id()
                    _await_event_: AwaitEvent = AwaitEvent()
                    self._active_requests[_request_id_] = _await_event_
                    _object_exists_response_: Response = patch(
                        f"{self.base_url}/{self.__tablename__}/{self.id}",
                        json={name: value},
                    )
                    _object_exists_response_.raise_for_status()
                    the_redis_client._.publish(
                        "updated",
                        dumps({"object_id": str(self.id), "request_id": str(_request_id_)}),
                    )
                    _await_event_.wait()
                    return
            super().__setattr__(name, value)

    _AutoCreate.default_base_url = default_base_url

    return _AutoCreate
