from django import forms

from .models import Fund

HINT_MESSAGE = (
    "Если фонд охватывает всю страну, то нужно указывать ТОЛЬКО страну. "
    "Если фонд охватывает весь регион, то нужно указывать ТОЛЬКО регион."
)


class FundAdminForm(forms.ModelForm):
    def clean(self):
        regions = list(self.cleaned_data["regions"])
        countries = list(self.cleaned_data["countries"])
        if not regions and not countries and not self.cleaned_data["cities"]:
            raise forms.ValidationError("Укажите охват фонда.")
        not_valid_cities = [
            city.name
            for city in self.cleaned_data["cities"]
            if city.region in regions or city.region.country in countries
        ]
        if not_valid_cities:
            raise forms.ValidationError(
                f"Вместе с городами {not_valid_cities} указаны их " f"регионы или страны. {HINT_MESSAGE}"
            )
        not_valid_regions = [region.name for region in regions if region.country in countries]
        if not_valid_regions:
            raise forms.ValidationError(f"Вместе с регионами {not_valid_regions} указаны их страны. " f"{HINT_MESSAGE}")

    class Meta:
        model = Fund
        fields = "__all__"
