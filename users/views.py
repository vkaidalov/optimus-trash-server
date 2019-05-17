from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from .models import User
from .permissions import (
    IsAccountOwnerOrReadOnly,
    IsSuperUser,
    IsConfirmedOrReadOnly
)
from .serializers import UserSerializer, ConfirmationSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter)
    filterset_fields = ('is_confirmed',)
    search_fields = ('username',)
    ordering_fields = ('date_joined',)


class UserDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAccountOwnerOrReadOnly,
                          IsConfirmedOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserConfirmation(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,
                          IsSuperUser)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *_args, **_kwargs):
        user = self.get_object()
        confirmation_serializer = ConfirmationSerializer(data=request.data)

        if not confirmation_serializer.is_valid():
            return Response(confirmation_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        user.is_confirmed = confirmation_serializer.save()
        user.save()

        return Response(confirmation_serializer.validated_data,
                        status.HTTP_201_CREATED)
