"""
Celery tasks for batch processing records.
"""

import requests

from celery import shared_task

from records.logger import logger


EXTERNAL_API_URL = 'https://dev.micro.mgsigma.net/batch/process'
BATCH_SIZE = 10


@shared_task(bind=True, max_retries=3)
def process_batch(self):
    """
    Fetch up to 10 PENDING/FAILED records and send to external API.
    Update status based on response.
    
    Runs every 2 hours via Celery Beat.
    """
    # Import here to avoid circular imports
    from records.models import Record
    
    logger.info("Starting batch processing task")
    
    # Fetch records that need processing (PENDING or FAILED)
    records = Record.objects.filter(
        status__in=[Record.Status.PENDING, Record.Status.FAILED]
    ).order_by('created_at')[:BATCH_SIZE]
    
    if not records:
        logger.info("No records to process")
        return {'processed': 0, 'message': 'No records to process'}
    
    logger.info(f"Found {len(records)} records to process")
    
    # Prepare batch payload
    payload = []
    for record in records:
        record_data = {
            'id': record.id,
            'name': record.name,
            'email': record.email,
            'phoneNumber': record.phone_number,
            'link': record.link or '',
            'dob': record.dob.strftime('%d/%m/%Y') if record.dob else ''
        }
        payload.append(record_data)
    
    logger.debug(f"Sending payload: {payload}")
    
    try:
        # Send to external API
        response = requests.post(
            EXTERNAL_API_URL,
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        response.raise_for_status()
        
        # Process response
        results = response.json()
        logger.info(f"Received response: {results}")
        
        # Update record statuses based on response
        success_count = 0
        failed_count = 0
        
        for result in results:
            record_id = result.get('id')
            status = result.get('status')
            
            try:
                record = Record.objects.get(id=record_id)
                if status == 'SUCCESS':
                    record.status = Record.Status.SUCCESS
                    success_count += 1
                    logger.info(f"Record {record_id} marked as SUCCESS")
                else:
                    record.status = Record.Status.FAILED
                    failed_count += 1
                    logger.warning(f"Record {record_id} marked as FAILED")
                record.save()
            except Record.DoesNotExist:
                logger.error(f"Record {record_id} not found in database")
        
        return {
            'processed': len(results),
            'success': success_count,
            'failed': failed_count
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"External API request failed: {str(e)}")
        # Retry the task
        raise self.retry(exc=e, countdown=60)
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        raise
