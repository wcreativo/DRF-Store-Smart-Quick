import csv
import pandas as pd
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from .models import Client, Product, Bill
from .serializers import ClientSerializer, ProductSerializer, BillSerializer, UploadSerializer
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


class ClientLoader(APIView):
    serializer_class = UploadSerializer
    valid_file_types = [
        'text/csv'
    ]

    def post(self, request):
        errors = []
        serializer_client = UploadSerializer(data=request.data)

        if not serializer_client.is_valid():
            return Response(serializer_client.errors, status=status.HTTP_400_BAD_REQUEST)

        file_uploaded = request.FILES.get('file_uploaded')

        if file_uploaded is None:
            return Response({'detail': 'No file selected'}, status=400)

        content_type = file_uploaded.content_type

        if content_type not in self.valid_file_types:
            return Response({'detail': f'Invalid file type {content_type}'}, status=400)

        try:
            df = pd.read_csv(file_uploaded)
        except Exception as e:
            errors.append(e)
            df = None

        for i in df.index:
            try:
                Client.objects.create(first_name=df['first_name'][i], last_name=df['last_name'][i],
                                      document=df['document'][i], email=df['email'][i])
            except Exception as e:
                errors.append(e)
        if errors:
            return Response({'detail': errors}, status=status.HTTP_201_CREATED)

        return Response({}, status=200)
