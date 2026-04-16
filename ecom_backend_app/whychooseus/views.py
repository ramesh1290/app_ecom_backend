from rest_framework import generics
from .models import WhyChooseUs
from .serializers import WhyChooseUsSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
# GET (list) + POST
class WhyChooseUsListCreateView(generics.ListCreateAPIView):
    queryset = WhyChooseUs.objects.all().order_by("order")
    serializer_class = WhyChooseUsSerializer


#  GET (single) + PATCH + DELETE
class WhyChooseUsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WhyChooseUs.objects.all()
    serializer_class = WhyChooseUsSerializer

@api_view(["POST"])
def reorder_why_choose_us(request):
    order = request.data.get("order", [])

    for index, item_id in enumerate(order):
        WhyChooseUs.objects.filter(id=item_id).update(order=index)

    return Response({"message": "Order updated"})