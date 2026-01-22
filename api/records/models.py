from django.db import models

from records.logger import logger


class Record(models.Model):
    """
    Model to store form submission records.
    Status tracks the batch processing state.
    """
    
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=20,
        help_text="International format with country code (e.g., +919876543210)"
    )
    link = models.URLField(
        blank=True, 
        null=True,
        help_text="Portfolio, GitHub, or LinkedIn URL"
    )
    dob = models.DateField(
        blank=True, 
        null=True,
        help_text="Date of birth"
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True  # Index for faster filtering
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Record'
        verbose_name_plural = 'Records'
    
    def __str__(self):
        return f"{self.name} ({self.email}) - {self.status}"
    
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            logger.info(f"New record created: {self.name} (ID: {self.pk})")
        else:
            logger.debug(f"Record updated: {self.name} (ID: {self.pk}, Status: {self.status})")
