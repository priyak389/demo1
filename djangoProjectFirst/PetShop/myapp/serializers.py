from rest_framework import serializers
from .models import customerDetails
class customerSerializer(serializers.ModelSerializer):
    class Meta:
        model=customerDetails
        fields='__all__'
        
