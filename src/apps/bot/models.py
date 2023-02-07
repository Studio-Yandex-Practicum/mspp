from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class BaseModel(models.Model):
    """
    An abstract base class model.

    It provides self-updating ``created_at`` and ``updated_at`` fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.id}"


class CoverageArea(MPTTModel, BaseModel):
    name = models.CharField(
        verbose_name="название",
        max_length=100,
        unique=True,
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="родительская зона охвата",
    )

    class MPTTMeta:
        order_insertion_by = ("name",)

    class Meta:
        verbose_name = "зона охвата"
        verbose_name_plural = "зоны охвата"

    def __str__(self):
        return self.name


class AgeLimit(BaseModel):
    """
    AgeLimit class model.

    It provides ``from_age`` and ``to_age`` fields.
    """

    from_age = models.PositiveSmallIntegerField(
        verbose_name="нижняя граница",
        null=True,
        blank=True,
    )
    to_age = models.PositiveSmallIntegerField(
        verbose_name="верхняя граница",
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ("from_age", "to_age")
        verbose_name = "возрастное ограничение"
        verbose_name_plural = "возрастные ограничения"
        constraints = [
            models.UniqueConstraint(
                fields=("from_age", "to_age"),
                name="диапазон возрастов должен быть уникальным",
            ),
            models.UniqueConstraint(
                fields=("from_age",),
                name=("значение нижней границы, при не указанном верхнем, " "должно быть уникальным"),
                condition=models.Q(to_age__isnull=True),
            ),
            models.UniqueConstraint(
                fields=("to_age",),
                name=("значение верхней границы, при не указанном нижнем, " "должно быть уникальным"),
                condition=models.Q(from_age__isnull=True),
            ),
            models.CheckConstraint(
                check=~models.Q(from_age=None, to_age=None), name="нужно указать хотя бы одно значение"
            ),
            models.CheckConstraint(
                check=models.Q(from_age__lte=models.F("to_age")), name="нижняя граница не может быть больше верхней"
            ),
        ]

    def __str__(self):
        result = []
        if self.from_age is not None:
            result.append(f"от {self.from_age}")
        if self.to_age is not None:
            result.append(f"до {self.to_age}")
        return " ".join(result)


class Fund(BaseModel):
    """Fund class model."""

    name = models.CharField(
        verbose_name="название",
        max_length=256,
    )
    coverage_area = TreeManyToManyField(CoverageArea, related_name="funds", verbose_name="зоны охвата")
    age_limit = models.ForeignKey(
        AgeLimit,
        verbose_name="возрастные ограничения",
        on_delete=models.PROTECT,
    )
    description = models.TextField(verbose_name="описание")

    class Meta:
        ordering = ("name",)
        verbose_name = "фонд"
        verbose_name_plural = "фонды"

    def __str__(self):
        return self.name
