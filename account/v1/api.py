from rest_framework import viewsets, mixins, status,serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import Http404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from account.models import RequestCount
from django.db.models import Sum

from .serializers import RegisterUserSerializer

class RegistrationView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        serialized = RegisterUserSerializer(data=request.data, context={'request': request})

        if serialized.is_valid(raise_exception=True):
            user = serialized.create()
            serializer = TokenObtainPairSerializer(data=request.data)
            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])
            data = {'access_token': serializer.validated_data.get('access')}
            return Response(data, status=status.HTTP_200_OK)
        raise Http404


class RequestContView(viewsets.GenericViewSet):
    serializer_class = serializers.Serializer
    
    def list(Self, request):
        requests_counts = RequestCount.objects.only('count').first()
        if requests_counts:
            return Response({'requests':requests_counts.count}, status=status.HTTP_200_OK)
        
        return Response({}, status=status.HTTP_200_OK)
        
    
    @action(methods=['POST'], detail=False)
    def rest(self, request):
        RequestCount.objects.all().delete()
        return Response({}, status=status.HTTP_200_OK)