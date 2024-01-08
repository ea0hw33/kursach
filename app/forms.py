from django.forms import ModelForm

from app.models import *


class participateInNIRstud(ModelForm):
    class Meta:
        model = uchastnikyOnNIR
        fields = ["student","nir","isParticipent"]