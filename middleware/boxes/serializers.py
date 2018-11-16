from .models import BoxStatus
from .models import Script
from .models import Patches
from .models import UpdateInformation
from rest_framework import serializers


class BoxStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxStatus
        fields = '__all__'


class ScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Script
        fields = '__all__'


class PatchesSerializer(serializers.ModelSerializer):

    scripts = ScriptSerializer(many=True)

    class Meta:
        model = Patches
        fields = ("id", "name", "scripts")
