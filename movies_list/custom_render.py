from rest_framework import renderers
from django.http import JsonResponse
from rest_framework.views import exception_handler
from rest_framework.renderers import JSONRenderer
class ApiResponse(JSONRenderer):
    def render(self, data, media_type=None, renderer_context=None):
        try:
            exception = data.get('exception', None)
        except:
            exception = None
        try:
            success_message = data.get('success_message_head', None)
            del data['success_message_head']
        except Exception as e:
            success_message = None
        request = renderer_context.get('request', None)
        isMobile = request.query_params.get('is_mobile', None)
        # isMobile = True
        if isMobile :
            if exception:
                    del data['exception']
                    code = data['status']['code']
                    staus = data['status']['state']
                    message = data['status']['message']
                    del data['status']
                    response_data = {'data': data, 'response': {'status': staus, 'code': code, 'message': message}}
            else:
                response_data = {'data': data, 'response': {'status': 'success',
                                                            'code': renderer_context['response'].status_code}}
        else:
            if exception:
                    del data['exception']
                    code = data['status']['code']
                    staus = data['status']['state']
                    message = data['status']['message']
                    del data['status']
                    status_data = {'status': staus, 'code': code, 'message': message}
                    response_data = {'data': data, 'status': status_data}
            else:
                status = {'status': 'success', 'code': renderer_context['response'].status_code}
                response_data = {'data': data, 'status': status}
        if success_message:
            response_data['status']['message'] = [{'message': success_message, 'id': 'message'}]
        if 'message' not in response_data['status']:
            response_data['status']['message'] = []
        return super(ApiResponse, self).render(response_data, media_type, renderer_context)