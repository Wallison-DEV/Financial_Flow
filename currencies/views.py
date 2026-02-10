from rest_framework import permissions, viewsets

from .serializers import CurrencySerializer
from .models import CurrencyModel

class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = CurrencyModel.objects.all().order_by('name')
    serializer_class = CurrencySerializer
    permission_classes = [permissions.IsAuthenticated]
