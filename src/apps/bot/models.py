from django.db import models


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


class Country(BaseModel):
    name = models.CharField(
        verbose_name="название",
        max_length=100,
        unique=True,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "страна"
        verbose_name_plural = "страны"

    def __str__(self):
        return self.name


class Region(BaseModel):
    name = models.CharField(
        verbose_name="название",
        max_length=100,
        unique=True,
    )
    country = models.ForeignKey(
        Country,
        verbose_name="страна",
        on_delete=models.CASCADE,
        related_name="regions",
    )

    class Meta:
        ordering = (
            "country__name",
            "name",
        )
        verbose_name = "регион"
        verbose_name_plural = "регионы"

    def __str__(self):
        return f"{self.name}, {self.country}"


class City(BaseModel):
    """City class model."""

    name = models.CharField(
        verbose_name="название",
        max_length=100,
    )
    region = models.ForeignKey(Region, verbose_name="регион", on_delete=models.CASCADE, related_name="cities")

    class Meta:
        ordering = (
            "region__country__name",
            "region__name",
            "name",
        )
        verbose_name = "город"
        verbose_name_plural = "города"
        constraints = [models.UniqueConstraint(fields=["name", "region"], name="Unique city in region")]

    def __str__(self):
        return f"{self.name}, {self.region}"


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
                fields=["from_age", "to_age"],
                name="Unique age limit",
            ),
            models.CheckConstraint(
                check=~models.Q(from_age=None, to_age=None), name="Нужно указать хотя бы одно значение"
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
    countries = models.ManyToManyField(
        Country,
        verbose_name="страны",
        blank=True,
        related_name="funds",
    )
    regions = models.ManyToManyField(
        Region,
        verbose_name="регионы",
        blank=True,
        related_name="funds",
    )
    cities = models.ManyToManyField(
        City,
        verbose_name="города",
        blank=True,
        related_name="funds",
    )
    age_limit = models.ForeignKey(
        AgeLimit,
        verbose_name="возрастные ограничения",
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "фонд"
        verbose_name_plural = "фонды"

    def __str__(self):
        return self.name
