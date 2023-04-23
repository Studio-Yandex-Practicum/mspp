from django import forms

from .models import Fund

COVERAGE_ERROR_MESSAGE = (
    "Для зон охвата {coverages} указаны их дочерние зоны. "
    "Если фонд охватывает всю страну, то нужно указывать ТОЛЬКО страну. "
    "Если фонд охватывает весь регион, то нужно указывать ТОЛЬКО регион."
)


class FundAdminForm(forms.ModelForm):
    def clean(self):
        coverages = list(self.cleaned_data.get("coverage_area", []))
        not_valid_ancestors = {
            ancestor.name for ancestor in coverages for coverage in coverages if ancestor.is_ancestor_of(coverage)
        }
        if not_valid_ancestors:
            raise forms.ValidationError(COVERAGE_ERROR_MESSAGE.format(coverages=not_valid_ancestors))

    class Meta:
        model = Fund
        fields = "__all__"
