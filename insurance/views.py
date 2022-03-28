from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from insurance.serializers import CustomerSerializer, PolicySerializer
from insurance.models import Customer, Policy
from rest_framework.views import APIView
from insurance.logic.csv_import import importCsvFile
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth


class CustomerViewSet(APIView):
    def get(self, request, id):
        queryset = Customer.objects
        if id:
            queryset = queryset.filter(id=id)
        serializer = CustomerSerializer(queryset.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnalyticsViewSet(APIView):
    def get(self, request, region):
        policy = Policy.objects.select_related('customer_id')
        if region:
            policy = policy.filter(customer_id__region=region)
        policy = policy.annotate(month=TruncMonth('date_of_purchase')).values(
            'month').annotate(count=Count('policy_id')).values('month', 'count')
        return Response(policy, status=status.HTTP_200_OK)


class AllDataViewSet(APIView):
    def get(self, request, dt):
        customer = request.GET["customer"]
        policy = request.GET["policy"]
        queryset = Policy.objects.prefetch_related(
            'customer_id')
        if customer != 'All':
            queryset = queryset.filter(customer_id=customer)
        if policy != 'All':
            queryset = queryset.filter(policy_id=policy)
        serializer = PolicySerializer(queryset, many=True)
        return Response(serializer.data[int(dt):int(dt)+10], status=status.HTTP_200_OK)

    def patch(self, request, dt):
        data = request.data
        sum = Policy.objects.filter(
            customer_id=data['previous']['customer_id']).aggregate(Sum('premium'))
        if float(sum['premium__sum']) + float(data['new']['premium']) <= 1000000:
            try:
                policy = Policy.objects.get(pk=dt)
                policy.fuel_type = data['new']['fuel']
                policy.vehicle_segment = data['new']['vehicle']
                policy.premium = data['new']['premium']
                policy.body_injury_liability = data['new']['bodyLiability']
                policy.personal_injury_liability = data['new']['personalLiability']
                policy.property_injury_liability = data['new']['propertylLiability']
                policy.collision_liability = data['new']['collisionLiability']
                policy.comprehensive_liability = data['new']['comprehensivelLiability']
                policy.save()
                pl = Policy.objects.filter(pk=dt)
                serializer = PolicySerializer(pl, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Exception as E:
                return Response(str(E), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(f"Maximum 1M is allowed found {sum['premium__sum'] + float(data['new']['premium'])}", status=status.HTTP_202_ACCEPTED)


class PolicyViewSet(APIView):
    def get(self, request):
        queryset = Policy.objects.all()
        serializer = PolicySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PolicySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            data = serializer.data
            return(data)


class UploadCSV(APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request, format=None):
        # res = importCsvFile(request.data)
        res = importCsvFile(request.FILES)
        return Response({'received data': res})
