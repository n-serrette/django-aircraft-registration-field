from django.forms import Select, TextInput
from django.forms.widgets import MultiWidget
from django_countries.fields import Country
from .data import COUNTRIES_PREFIX


class AircraftRegistrationPrefixSelect(Select):
    initial = None

    def __init__(self, initial=None):
        choices = [("", "---------")]
        for country_code, prefix in COUNTRIES_PREFIX:
            country = Country(country_code)
            if country:
                choices.append((prefix, "%s %s" % (country.name, prefix)))
        choices = sorted(choices, key=lambda item: item[1])
        # TODO imitate django_countries?
        # if initial:
        #     country = Country(initial)
        #     if country:
        #         choices.insert(0, "%s %s" % (country.name, initial))
        super().__init__(
            choices=choices
        )


class AircraftRegistrationPrefixWidget(MultiWidget):

    def __init__(self, attrs=None, initial=None):
        widgets = (
            AircraftRegistrationPrefixSelect(initial),
            TextInput(attrs=attrs)
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            possibility = [x[1] for x in COUNTRIES_PREFIX
                           if value.startswith(x[1])]
            if len(possibility) == 0:
                return [None, ""]
            prefix = max(possibility, key=len)
            id = value.replace(prefix, '')
            return [prefix, id]
        return [None, ""]

    def value_from_datadict(self, data, files, name):
        parts = [widget.value_from_datadict(data, files, name + '_%s' % i)
                 for i, widget in enumerate(self.widgets)]
        parts = [x if x else '' for x in parts]
        return ''.join(parts)
