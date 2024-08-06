from rest_framework import serializers
from .models import EmpID


class EmpIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmpID
        fields = ['emp_id']
