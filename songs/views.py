from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Song
from rest_framework.pagination import PageNumberPagination
from .serializers import SongSerializer
from albums.models import Album
from rest_framework import generics


class SongView(generics.ListCreateAPIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Song.objects.all()
    serializer_class = SongSerializer
    lookup_url_kwarg = "pk"
    

    def get_queryset(self):
        pk = self.kwargs[self.lookup_url_kwarg]
        return Song.objects.filter(album_id=pk)

    def perform_create(self, serializer):
        pk = self.kwargs[self.lookup_url_kwarg]
        album = get_object_or_404(Album, id=pk)
        serializer.is_valid(raise_exception=True)
        serializer.save(album_id=album.id)