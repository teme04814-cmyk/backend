from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializers import DocumentSerializer


class IsUploaderOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.uploader == request.user


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated, IsUploaderOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        user = self.request.user
        qs = Document.objects.all() if user.is_staff else Document.objects.filter(uploader=user)
        try:
            params = getattr(self.request, "query_params", {}) or {}
            vehicle_id = params.get("vehicle") or params.get("vehicle_id")
            if vehicle_id:
                try:
                    qs = qs.filter(vehicle_id=vehicle_id)
                except Exception:
                    pass
            app_id = params.get("application") or params.get("application_id")
            if app_id:
                try:
                    qs = qs.filter(application_id=app_id)
                except Exception:
                    pass
            uploader_id = params.get("uploader") or params.get("uploader_id")
            if uploader_id and user.is_staff:
                try:
                    qs = qs.filter(uploader_id=uploader_id)
                except Exception:
                    pass
        except Exception:
            pass
        return qs

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            if not request.FILES.get("file") and not request.data.get("file"):
                return Response({"detail": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
            if request.data.get("name") and "name" not in request.data:
                request.data["name"] = request.data.get("name")
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
