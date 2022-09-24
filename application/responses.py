from datetime import datetime
from time import mktime

from bson import ObjectId
from rest_framework import status
from rest_framework.response import Response
from bson import json_util
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.encoders import JSONEncoder
# from rest_framework.utils import json


class RestResponse(Response):
    
    def load_data(self, data):
        return json.loads(json_util.dumps(data))

    def __init__(self, data=None, message=None, data_status=True, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None, lead_counts=0, agent_counts=0):
        data_content = {
            'status': data_status,
            'message': message,
            'data': self.load_data(data)
        }
        
        if lead_counts:
            data_content = {
                'status': data_status,
                'message': message,
                'data': data,
                'lead_counts': lead_counts
            }
        elif agent_counts:
            data_content = {
                'status': data_status,
                'message': message,
                'data': data,
                'agent_counts': agent_counts
            }
        super(RestResponse, self).__init__(
            data=data_content
        )


class AccessDeniedResponse(RestResponse):
    status_code = status.HTTP_401_UNAUTHORIZED

class ConflictResponse(RestResponse):
    status_code = status.HTTP_409_CONFLICT

class BadRequestResponse(RestResponse):
    status_code = status.HTTP_400_BAD_REQUEST

class LockedRequestResponse(RestResponse):
    status_code = status.HTTP_423_LOCKED

class SuccessResponse(RestResponse):
    status_code = status.HTTP_200_OK


class CreateResponse(RestResponse):
    status_code = status.HTTP_201_CREATED


class NotFoundResponse(RestResponse):
    status_code = 404


class NotImplemented(RestResponse):
    status_code = 501

class ServerError(RestResponse):
    status_code = 500


class NoContentResponse(RestResponse):
    status_code = status.HTTP_204_NO_CONTENT


class UnauthorizedResponse(RestResponse):
    status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenErrorResponse(RestResponse):
    status_code = status.HTTP_403_FORBIDDEN

class ForbiddenResponse(RestResponse):
    status_code = status.HTTP_403_FORBIDDEN

class UnprocessableEntityResponse(RestResponse):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY


class NotAcceptableResponse(RestResponse):
    status_code = status.HTTP_406_NOT_ACCEPTABLE

class MethodNotAllowedResponse(RestResponse):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED

class ResourceNotFoundResponse(RestResponse):
    status_code = status.HTTP_404_NOT_FOUND