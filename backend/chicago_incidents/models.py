from django.db import models


class AutoCreatedUpdatedModel(models.Model):
    """Abstract model for entities that track creation and update date.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Incident(AutoCreatedUpdatedModel):
    """Model for incident requests
    """
    OPEN = 'OPEN'
    OPEN_DUP = 'OPEN_DUP'
    CLOSED = 'CLOSED'
    CLOSED_DUP = 'CLOSED_DUP'
    STATUS_TYPE_CHOICES = [
        (OPEN, 'Open'), (OPEN_DUP, 'Open - Dup'), (CLOSED, 'Closed'), (CLOSED_DUP, 'Closed - Dup')
    ]

    ABANDONED_VEHICLE = 'ABANDONED_VEHICLE'
    ALLEY_LIGHT_OUT = 'ALLEY_LIGHT_OUT'
    GARBAGE_CART = 'GARBAGE_CART'
    GRAFFITI = 'GRAFFITI'
    POT_HOLE = 'POT_HOLE'
    RODENT_BAITING = 'RODENT_BAITING'
    SANITATION_CODE = 'SANITATION_CODE'
    STREET_LIGHTS_ALL_OUT = 'STREET_LIGHTS_ALL_OUT'
    STREET_LIGHT_ONE_OUT = 'STREET_LIGHT_ONE_OUT'
    TREE_DEBRIS = 'TREE_DEBRIS'
    TREE_TRIM = 'TREE_TRIM'
    SERVICE_TYPE_CHOICES = [
        (ABANDONED_VEHICLE, 'Abandoned Vehicle Complaint'),
        (ALLEY_LIGHT_OUT, 'Alley Light Out'),
        (GARBAGE_CART, 'Garbage Cart Black Maintenance/Replacement'),
        (GRAFFITI, 'Graffiti Removal'),
        (POT_HOLE, 'Pothole in Street'),
        (RODENT_BAITING, 'Rodent Baiting/Rat Complaint'),
        (SANITATION_CODE, 'Sanitation Code Violation'),
        (STREET_LIGHTS_ALL_OUT, 'Street Lights - All/Out'),
        (STREET_LIGHT_ONE_OUT, 'Street Light Out'),
        (TREE_DEBRIS, 'Tree Debris'),
        (TREE_TRIM, 'Tree Trim')
    ]

    creation_date = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_TYPE_CHOICES)
    completion_date = models.DateTimeField(null=True, blank=True)
    service_request_number = models.CharField(max_length=20)
    type_of_service_request = models.CharField(max_length=30, choices=SERVICE_TYPE_CHOICES)
    current_activity = models.CharField(max_length=30, null=True, blank=True)
    most_recent_action = models.CharField(max_length=30, null=True, blank=True)
    street_address = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.IntegerField(null=True, blank=True)
    zip_codes = models.IntegerField(null=True, blank=True)
    x_coordinate = models.DecimalField(max_digits=25, decimal_places=10, null=True, blank=True)
    y_coordinate = models.DecimalField(max_digits=25, decimal_places=10, null=True, blank=True)
    ward = models.IntegerField(null=True, blank=True)
    wards = models.IntegerField(null=True, blank=True)
    historical_wards_03_15 = models.IntegerField(null=True, blank=True)
    police_district = models.IntegerField(null=True, blank=True)
    community_area = models.IntegerField(null=True, blank=True)
    community_areas = models.IntegerField(null=True, blank=True)
    ssa = models.IntegerField(null=True, blank=True)
    census_tracts = models.IntegerField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=30, decimal_places=20, null=True, blank=True)
    longitude = models.DecimalField(max_digits=30, decimal_places=20, null=True, blank=True)
    location = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'incidents'

    def __str__(self):
        """Return the string representation of the incident.

        :return: The service request number.
        """
        return self.service_request_number


# TODO add foreign keys to incidents table
# class AbandonedCar(AutoCreatedUpdatedModel):
#     """Model for abandoned cars
#     """

# class Graffiti(AutoCreatedUpdatedModel):
#     """Model for graffities
#
# etc.
