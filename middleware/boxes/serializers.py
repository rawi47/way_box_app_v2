from .models import Patch, Script
from rest_framework import serializers


class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = '__all__'


class PatchesSerializer(serializers.ModelSerializer):

    scripts = ScriptSerializer(many=True)

    class Meta:
        model = Patch
        fields = ("id", "name", "scripts")
