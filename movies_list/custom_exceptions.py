from rest_framework.views import exception_handler
from rest_framework.utils.serializer_helpers import ReturnDict
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response is not None:
        if response.status_code >= 400 and response.status_code < 500:
            response_data_errors = []
            if isinstance(response.data, ReturnDict):
                for key in response.data:
                    value = response.data[key]
                    response_data_dic = {}
                    response_data_dic['id'] = key
                    if isinstance(value, list):
                        value = value[0]
                    response_data_dic['error'] = value
                    response_data_errors.append(response_data_dic)
            elif isinstance(response.data, list):
                for err in response.data:
                    response_data_errors.append({
                        'id':'',
                        'error': response.data[err]
                    })
            elif isinstance(response.data, dict):
                if 'detail' in response.data:
                    response_data_errors.append({
                        'id': '',
                        'error': response.data['detail']
                    })
                else:
                    for keys in response.data:
                        response_data_errors.append({
                            'id': keys,
                            'error': response.data[keys]
                        })
            response.data = dict()
        if 200 <= response.status_code < 300:
            response_code = response.status_code
            response.status_code = 200
            response.data['status'] = {'code': response_code, 'state': 'success',
                                       'message': [{'id': 'details', 'message': 'Request successful.'}]}
        elif 400 <= response.status_code < 500:
            response_code = response.status_code
            response.status_code = 200
            response.data['status'] = {'code': response_code, 'state': 'failure', 'message': response_data_errors}
        response.data['exception'] = True
    return response