from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.permissions import IsConfirmedOrReadOnly
from .models import Bin
from .serializers import BinSerializer


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


class BinDetail(generics.RetrieveAPIView):
    queryset = Bin.objects.all()
    serializer_class = BinSerializer
