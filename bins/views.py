from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics
from .models import Bin
from .serializers import BinSerializer


class BinList(generics.ListAPIView):
    queryset = Bin.objects.all().order_by('id')
    serializer_class = BinSerializer
    filter_backends = (filters.OrderingFilter,
                       DjangoFilterBackend)
    ordering_fields = ('fullness',)
    filterset_fields = ('owner',)


class BinDetail(generics.RetrieveAPIView):
    queryset = Bin.objects.all()
    serializer_class = BinSerializer
