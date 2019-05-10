from rest_framework import generics
from rest_framework import permissions
from .models import User
from .permissions import IsAccountOwnerOrReadOnly
from .serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsAccountOwnerOrReadOnly)
    queryset = User.objects.all()
    serializer_class = UserSerializer
