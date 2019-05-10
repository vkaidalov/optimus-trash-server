from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from .models import User
from .permissions import IsAccountOwnerOrReadOnly, IsSuperUser
from .serializers import UserSerializer, ConfirmationSerializer


class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        This specifies filters, such as `username_contains`, `is_confirmed`.
        """
        queryset = User.objects.all().order_by('id')

        username_contains = self.request.query_params.get(
            'username_contains', None
        )
        if username_contains is not None:
            queryset = queryset.filter(username__contains=username_contains)

        is_confirmed = self.request.query_params.get(
            'is_confirmed', None
        )
        is_confirmed = True if is_confirmed == 'true' \
            else False if is_confirmed == 'false' \
            else None
        if is_confirmed is not None:
            queryset = queryset.filter(is_confirmed=is_confirmed)

        return queryset


class UserDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAccountOwnerOrReadOnly)
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
