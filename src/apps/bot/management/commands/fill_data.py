import json
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db.models import Max

from ...models import AgeLimit, CoverageArea, Fund

DATA_DIR = Path(__file__).resolve().parent / "data"


class Command(BaseCommand):
    def handle(self, *args, **options):
        Fund.objects.all().delete()
        AgeLimit.objects.all().delete()
        if CoverageArea.objects.count():
            for level in range(CoverageArea.objects.aggregate(Max("level"))["level__max"], -1, -1):
                CoverageArea.objects.filter(level=level).delete()
        with (DATA_DIR / "coveragearea.json").open() as file:
            areas = json.load(file)
            areas_db = CoverageArea.objects.bulk_create(
                [CoverageArea(name=area["name"], level=0, lft=0, rght=0, tree_id=0) for area in areas]
            )
            for area, area_db in zip(areas, areas_db):
                parent_name = area["parent"]
                if parent_name is not None:
                    area_db.parent = CoverageArea.objects.get(name=parent_name)
            CoverageArea.objects.bulk_update(areas_db, fields=("parent",))
            CoverageArea.objects.rebuild()
        with (DATA_DIR / "agelimit.json").open() as file:
            AgeLimit.objects.bulk_create([AgeLimit(**age_limit) for age_limit in json.load(file)])
        with (DATA_DIR / "fund.json").open() as file:
            funds = json.load(file)
            funds_db = Fund.objects.bulk_create(
                [
                    Fund(
                        name=fund["name"],
                        description=fund["description"],
                        age_limit=AgeLimit.objects.get(
                            from_age=fund["age_limit"]["from_age"],
                            to_age=fund["age_limit"]["to_age"],
                        ),
                    )
                    for fund in funds
                ]
            )
            for fund, fund_db in zip(funds, funds_db):
                fund_db.coverage_area.set(CoverageArea.objects.filter(name__in=fund["coverage_area"]))
