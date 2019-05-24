from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)

from users.permissions import (
    IsConfirmedOrReadOnly, IsConfirmed
)
from .models import Bin
from .permissions import (
    IsBinOwnerOrReadOnly, IsBinOwner
)
from .serializers import BinSerializer, BinTokenSerializer


class BinList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsConfirmedOrReadOnly,)
    queryset = Bin.objects.all().order_by('id')
    serializer_class = BinSerializer
    filter_backends = (filters.OrderingFilter,
                       DjangoFilterBackend)
    ordering_fields = ('fullness',)
    filterset_fields = ('owner',)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BinDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,
                          IsConfirmedOrReadOnly,
                          IsBinOwnerOrReadOnly,)
    queryset = Bin.objects.all()
    serializer_class = BinSerializer


class BinTokenDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,
                          IsConfirmed,
                          IsBinOwner,)
    queryset = Bin.objects.all()
    serializer_class = BinTokenSerializer
