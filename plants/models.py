from django.db import models


class TimeStampedModel(models.Model):
    """Abstract base class that adds created_at and updated_at fields to models."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Location(TimeStampedModel):
    name = models.CharField(
        max_length=20,
        unique=True,
        blank=False,
        help_text="Name of location in the garden.",
    )

    def __str__(self):
        return f"name={self.name}"


class Pot(TimeStampedModel):
    name = models.CharField(
        max_length=30, unique=True, blank=False, help_text="Name of Pot/Container"
    )

    def __str__(self):
        return f"name={self.name}"


class Plant(TimeStampedModel):
    common_name = models.CharField(
        max_length=30,
        unique=False,
        null=False,
        blank=False,
        help_text="Common name (e.g. Strawberry)",
    )
    variety = models.CharField(
        max_length=30,
        null=True,
        blank=True,
        help_text="Variety name (e.g. Albion)",
    )
    species = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Species (e.g. Fragaria x ananassa)",
    )

    def __str__(self):
        return f"common_name={self.common_name}, variety={self.variety}, species={self.species}"


class Seed(TimeStampedModel):
    plant = models.ForeignKey(
        to=Plant, on_delete=models.CASCADE, help_text="Plant name, variety, species"
    )
    brand = models.CharField(
        max_length=20, null=True, blank=True, help_text="Brand name of seed"
    )
    source = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Source of seed (e.g. Encinal Nursery, Home)",
    )
    quantity = models.SmallIntegerField(
        null=True, blank=True, help_text="Quantity of Seed"
    )
    dt_germ = models.SmallIntegerField(
        null=True, blank=True, help_text="Days to Germination"
    )
    dt_harv = models.SmallIntegerField(
        null=True, blank=True, help_text="Days to Harvest"
    )
    purchase_date = models.DateField(null=True, blank=True, help_text="Purchase Date")
    exp_date = models.DateField(null=True, blank=True, help_text="Expiration Date")
    disposed_of = models.BooleanField(
        default=False, help_text="Has the seed been disposed of."
    )
    description = models.CharField(
        max_length=256, null=True, blank=True, help_text="Description of seed"
    )

    def __str__(self):
        return f"plant={self.plant.common_name}, variety={self.plant.variety}, species={self.plant.species}"


class Planting(TimeStampedModel):
    plant = models.ForeignKey(
        to=Plant,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Plant name, variety, species",
    )
    seed = models.ForeignKey(
        to=Seed,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Seed information if planted from seed",
    )
    pot = models.ForeignKey(
        to=Pot,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Pot if planted into container",
    )
    location = models.ForeignKey(
        to=Location,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        help_text="Location of planting",
    )
    brand = models.CharField(
        max_length=20, null=True, blank=True, help_text="Brand name of seed"
    )
    source = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="Source of seed (e.g. Encinal Nursery, Home)",
    )
    price = models.FloatField(
        null=True, blank=True, help_text="Cost of plant if purchased retail"
    )
    purchase_date = models.DateField(
        null=True, blank=True, help_text="Purchase Date if purchased retail"
    )
    seeding_date = models.DateField(
        null=True, blank=True, help_text="Seeding date if plant was seeded"
    )
    notes = models.CharField(
        max_length=256, null=True, blank=True, help_text="Notes about planting"
    )

    def __str__(self):
        if self.plant:
            fk_info = f"plant={self.plant.__str__()}"
        else:
            fk_info = f"seed={self.seed.__str__()}"
        if self.pot:
            loc_info = f"pot={self.pot.__str__()}"
        else:
            loc_info = f"location={self.location.__str__()}"
        return f"{fk_info}, {loc_info}"
