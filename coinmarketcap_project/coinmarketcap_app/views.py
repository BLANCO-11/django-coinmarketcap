from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Job, Task
from .serializers import JobSerializer, TaskSerializer
from .tasks import scrape_coin_data
import uuid

class StartScraping(APIView):
    def post(self, request):
        coins = request.data.get('coins', [])

        if not coins:
            return Response({"error": "No coins provided"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not all(isinstance(coin, str) for coin in coins):
            return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
        
        job = Job.objects.create()
        for coin in coins:
            task = Task.objects.create(job=job, coin=coin)
            scrape_coin_data.delay(task.id, coin)
            # print(task.id)
        
        return Response({"job_id": job.job_id}, status=status.HTTP_202_ACCEPTED)

class ScrapingStatus(APIView):
    def get(self, request, job_id):
        try:
            job = Job.objects.get(job_id=job_id)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = JobSerializer(job)
        return Response(serializer.data)
