from copy import deepcopy

from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView, CreateAPIView, DestroyAPIView, get_object_or_404
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from .models import Lesson, UserDetail, TimeBlock
from .services import check, get_users, main, check1


class Homepage(TemplateView):
    template_name = 'lessons_app/index.html'

    def get(self, request, *args, **kwargs):
        main()
        return super().get(request, *args, **kwargs)
