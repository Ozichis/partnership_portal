from django import forms
from .models import TargetChurch

class ChurchTargetForm(forms.ModelForm):
    class Meta:
        model = TargetChurch
        fields = "__all__"
    
    def save(self, commit=False):
        m = super(ChurchTargetForm, self).save(commit=commit)
        m.is_active = True
        m.save()
        return m