from pydantic import ValidationError
from schema import SCHEMA_MODEL
import json
from aiohttp import web


def get_http_error(error_class, message):
    error = error_class(
        text=json.dumps({"error": message}), content_type="application/json"
    )
    return error




def validate(model: SCHEMA_MODEL, data: dict):
    try:
        # return schema_cls(**json_data).dict(exclude_unset=True)
        return model.model_validate(data).model_dump(exclude_unset=True)
    except ValidationError as er:
        print(er)
        raise get_http_error(web.HTTPBadRequest, 'bad_request')

# def validate_user(schema_cls: USER_SCHEMA_CLASS, json_data: dict | list):
#     try:
#         return schema_cls(**json_data).dict(exclude_unset=True)
#     except ValidationError as er:
#         error = er.errors()[0]
#         error.pop('ctx', None)
#         raise HttpError(400, error)
