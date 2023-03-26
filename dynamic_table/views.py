from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import DynamicTableSerializer
from .permissions import DynamicTablePermission


class DynamicTableViewSet(viewsets.ViewSet):
    permission_classes = [DynamicTablePermission]

    def create(self, request):
        serializer = DynamicTableSerializer(data=request.data)
        if serializer.is_valid():
            model = serializer.save()
            return Response({"message": f"Table '{model.__name__}' created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
