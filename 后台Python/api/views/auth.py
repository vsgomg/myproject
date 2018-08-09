import json
from django.shortcuts import HttpResponse
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin

from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from rest_framework.pagination import PageNumberPagination

from api import models
from api.serializers.course import CourseSerializer,CourseModelSerializer
from api.utils.response import BaseResponse

class AuthView(ViewSetMixin,APIView):

    def login(self,request,*args,**kwargs):
        print('用户发来POST请求了',request)
        return Response({'code':11111})

