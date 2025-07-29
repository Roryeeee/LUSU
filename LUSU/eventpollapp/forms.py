from django import forms
from .models import Event, TimeOption, UserGroup
from django.forms import modelformset_factory


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'visible_to']

    # Limit groups to the ones the current user belongs to
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['visible_to'].queryset = user.user_groups.all()
        else:
            self.fields['visible_to'].queryset = UserGroup.objects.none()

class TimeOptionForm(forms.ModelForm):
    option = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

    class Meta:
        model = TimeOption
        fields = ['option']

TimeOptionFormSet = modelformset_factory(
    TimeOption,
    form=TimeOptionForm,
    extra=3,  # or dynamic with JS later
    can_delete=True
)