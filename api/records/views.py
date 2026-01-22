from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from records.models import Record
from records.serializers import RecordSerializer, RecordListSerializer
from records.logger import logger


class RecordCreateView(APIView):
    """
    POST /api/records/
    Create a new record from form submission.
    """
    
    def post(self, request):
        logger.info(f"Received record creation request: {request.data}")
        
        serializer = RecordSerializer(data=request.data)
        if serializer.is_valid():
            record = serializer.save()
            logger.info(f"Record created successfully: ID={record.id}")
            return Response(
                {
                    'message': 'Record created successfully',
                    'data': RecordSerializer(record).data
                },
                status=status.HTTP_201_CREATED
            )
        
        logger.warning(f"Record validation failed: {serializer.errors}")
        return Response(
            {
                'message': 'Validation failed',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class SuccessRecordsListView(APIView):
    """
    GET /api/records/success/
    List all records with SUCCESS status.
    """
    
    def get(self, request):
        logger.debug("Fetching SUCCESS records")
        
        records = Record.objects.filter(status=Record.Status.SUCCESS)
        serializer = RecordListSerializer(records, many=True)
        
        logger.info(f"Returning {records.count()} SUCCESS records")
        return Response(
            {
                'count': records.count(),
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
