import csv

from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from .models import Client, Product, Bill
from .serializers import ClientSerializer, ProductSerializer, BillSerializer
from rest_framework.response import Response


class ClientsList(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ProductsList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BillsList(generics.ListCreateAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class BillDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer


class ClientRecords(APIView):

    @staticmethod
    def get(request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="export.csv"'
        clients_records = Client.objects.raw('SELECT store_bill.id, COUNT(store_bill.id) AS bills_count, '
                                             'store_client.first_name, store_client.last_name, store_client.document '
                                             'FROM store_bill LEFT JOIN store_client ON store_bill.client_id = '
                                             'store_client.id GROUP BY store_bill.client_id')
        writer = csv.DictWriter(response, fieldnames=['document', 'full_name', 'bills_count'])
        writer.writeheader()
        for record in clients_records:
            writer.writerow({'document': record.document, 'full_name': f'{record.first_name} {record.last_name}',
                             'bills_count': record.bills_count})
        return response
