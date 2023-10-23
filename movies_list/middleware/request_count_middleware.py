from account.models import RequestCount
from decouple import config, Csv

class RequestCountMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):

        if not request.path_info.startswith(tuple(config('EXCLUDE_ENDPOINTS', default='/request-count', cast=Csv()))):

            request_count = RequestCount.objects.first() or RequestCount(count=0)
            request_count.count += 1
            request_count.save()
        response = self.get_response(request)
        
        
        return response
