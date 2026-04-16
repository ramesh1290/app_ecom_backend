from rest_framework import generics
from .models import About
from .serializers import AboutSerializer
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
# LIST + CREATE
class AboutListCreateView(generics.ListCreateAPIView):
    queryset = About.objects.all().order_by("-id")
    serializer_class = AboutSerializer


# RETRIEVE + UPDATE + DELETE
class AboutDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    