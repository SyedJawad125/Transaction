import ast
from django.db import models
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnList



class TimeStapms(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


def create_response(data, message, status_code):
    result = {
        "status_code": status_code,
        "message": message,
        "data": data
    }
    return Response(result, status=status_code)


def get_first_error_message_from_serializer_errors(serialized_errors, default_message=""):
    if not serialized_errors:
        return default_message
    try:
        serialized_error_dict = serialized_errors
        # ReturnList of serialized_errors when many=True on serializer
        if isinstance(serialized_errors, ReturnList):
            serialized_error_dict = serialized_errors[0]

        serialized_errors_keys = list(serialized_error_dict.keys())
        # getting first error message from serializer errors
        try:
            message = serialized_error_dict[serialized_errors_keys[0]][0].replace("This", serialized_errors_keys[0])
            return message
        except:
            return serialized_error_dict[serialized_errors_keys[0]][0]

    except Exception as e:
        return default_message


def get_params(name, instance, kwargs):
    instance = check_for_one_or_many(instance)
    if type(instance) == list or type(instance) == tuple:
        kwargs[f"{name}__in"] = instance
    else:
        kwargs[f"{name}"] = instance

    return kwargs

def check_for_one_or_many(instances):
    try:
        instance = ast.literal_eval(instances)
        print('from check_for_one_or_many')
        print(instance)
        return instance
    except Exception as e:
        print(e)
        return instances