import re
from datetime import date

from rest_framework import serializers

from records.models import Record
from records.logger import logger


class RecordSerializer(serializers.ModelSerializer):
    """
    Serializer for Record model with comprehensive server-side validation.
    """
    
    class Meta:
        model = Record
        fields = ['id', 'name', 'email', 'phone_number', 'link', 'dob', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']
    
    def validate_name(self, value):
        """Validate name is not empty and has reasonable length."""
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Name cannot be empty.")
        if len(value) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        if len(value) > 255:
            raise serializers.ValidationError("Name cannot exceed 255 characters.")
        return value
    
    def validate_email(self, value):
        """Validate email format."""
        value = value.strip().lower()
        # Basic email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise serializers.ValidationError("Invalid email format.")
        return value
    
    def validate_phone_number(self, value):
        """
        Validate phone number in international format.
        Format: +[country_code][number] (E.164 format)
        Examples: +919876543210, +14155552671
        """
        value = value.strip()
        # E.164 format: + followed by 1-15 digits
        phone_pattern = r'^\+[1-9]\d{1,14}$'
        if not re.match(phone_pattern, value):
            raise serializers.ValidationError(
                "Phone number must be in international format (e.g., +919876543210)."
            )
        return value
    
    def validate_link(self, value):
        """
        Validate optional URL field.
        Must be a valid URL if provided.
        """
        if not value:
            return None
        
        value = value.strip()
        # Basic URL pattern for portfolio/GitHub/LinkedIn
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(url_pattern, value, re.IGNORECASE):
            raise serializers.ValidationError("Invalid URL format. Must start with http:// or https://")
        return value
    
    def validate_dob(self, value):
        """
        Validate optional date of birth.
        Must be a valid date in the past if provided.
        """
        if not value:
            return None
        
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        
        # Reasonable age check (max 150 years old)
        min_date = date(date.today().year - 150, 1, 1)
        if value < min_date:
            raise serializers.ValidationError("Invalid date of birth.")
        
        return value
    
    def create(self, validated_data):
        """Create record and log the action."""
        record = super().create(validated_data)
        logger.info(f"Record created via API: ID={record.id}, Email={record.email}")
        return record


class RecordListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing records (SUCCESS status).
    """
    
    # Format DOB as DD/MM/YYYY for frontend display
    dob = serializers.SerializerMethodField()
    
    class Meta:
        model = Record
        fields = ['id', 'name', 'email', 'phone_number', 'link', 'dob', 'status', 'created_at']
    
    def get_dob(self, obj):
        """Format DOB as DD/MM/YYYY or None."""
        if obj.dob:
            return obj.dob.strftime('%d/%m/%Y')
        return None
