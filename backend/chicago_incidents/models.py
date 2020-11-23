from django.db import models
from django.db.models import Q
from rest_framework.exceptions import ValidationError


class AutoCreatedUpdatedModel(models.Model):
    """Helper abstract model for entities that track creation and update date at the database.
    This is completely irrelevant with the 'creation_date' & 'completion_date' of the incidents.
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
    COMPLETED = 'COMPLETED'
    COMPLETED_DUP = 'COMPLETED_DUP'
    STATUS_TYPE_CHOICES = [
        (OPEN, 'Open'), (OPEN_DUP, 'Open - Dup'), (COMPLETED, 'Completed'), (COMPLETED_DUP, 'Completed - Dup')
    ]

    ABANDONED_VEHICLE = 'ABANDONED_VEHICLE'
    ALLEY_LIGHTS_OUT = 'ALLEY_LIGHTS_OUT'
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
        (ALLEY_LIGHTS_OUT, 'Alley Lights Out'),
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
    street_address = models.CharField(max_length=100, null=True, blank=True)
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
        # Constraint to avoid duplication of data
        unique_together = [['creation_date', 'status', 'completion_date', 'service_request_number',
                           'type_of_service_request', 'street_address']
                           ]
        # The 1st index is useful for the importers
        indexes = [models.Index(fields=['creation_date', 'status', 'completion_date', 'service_request_number',
                                        'type_of_service_request', 'street_address']),
                   models.Index(fields=['creation_date']),
                   models.Index(fields=['zip_code']),
                   models.Index(fields=['type_of_service_request']),
                   ]

    def full_clean(self, exclude=None, validate_unique=True):
        if not self.completion_date and Incident.objects.exclude(id=self.id)\
                .filter(creation_date=self.creation_date, status=self.status, completion_date__isnull=True,
                        service_request_number=self.service_request_number,
                        type_of_service_request=self.type_of_service_request, street_address=self.street_address)\
                .exists():
            raise ValidationError("This incident already exists")
        super(Incident, self).full_clean()
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        return super(Incident, self).save()

    def __str__(self):
        """Return the string representation of the incident.

        :return: The service request number.
        """
        return self.service_request_number


class Activity(AutoCreatedUpdatedModel):
    """Model that holds the activities that applied to the incidents
    """
    current_activity = models.CharField(max_length=100, null=True, blank=True)
    most_recent_action = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'activities'
        # Constraint to avoid duplication of data
        unique_together = ['current_activity', 'most_recent_action']
        # The 1st index is useful for the importers
        indexes = [models.Index(fields=['current_activity', 'most_recent_action']), ]

    def clean(self):
        super().clean()
        if self.current_activity is None and self.most_recent_action is None:
            raise ValidationError("Activity fields are all None")


class ActivityIncident(AutoCreatedUpdatedModel):
    """Model that holds intermediate connection between activities and incidents
    """
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='activities_incidents')
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='activities_incidents')

    class Meta:
        db_table = 'activities_incidents'
        # Constraint to avoid duplication of data
        unique_together = ['activity', 'incident']


class AbandonedVehicle(AutoCreatedUpdatedModel):
    """Model for abandoned cars
    """
    license_plate = models.CharField(max_length=400, null=True, blank=True)
    vehicle_make_model = models.CharField(max_length=100, null=True, blank=True)
    vehicle_color = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'abandoned_vehicles'
        # Constraint to avoid duplication of data
        unique_together = ['license_plate', 'vehicle_make_model', 'vehicle_color']
        # The 1st index is useful for the importers
        indexes = [models.Index(fields=['license_plate', 'vehicle_make_model', 'vehicle_color']), ]

    def clean(self):
        super().clean()
        if self.license_plate is None and self.vehicle_color is None and self.vehicle_make_model is None:
            raise ValidationError("Abandoned vehicle fields are all None")

    def __str__(self):
        """Return the string representation of the incident.

        :return: The service request number.
        """
        return self.license_plate


class AbandonedVehicleIncident(AutoCreatedUpdatedModel):
    """Model that holds intermediate connection between abandoned vehicles and incidents. In that way we can hold one to
    many relations and more precisely a car can belong to multiple incidents (also it is supported many to many too,
    one incident can have multiple cars but this is not required)
    """
    abandoned_vehicle = models.ForeignKey(AbandonedVehicle, on_delete=models.CASCADE,
                                          related_name='abandoned_vehicles_incidents')
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='abandoned_vehicles_incidents')
    # THIS VALUE DIFFERS PER REQUEST!
    days_of_report_as_parked = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'abandoned_vehicles_incidents'
        # Constraint to avoid duplication of data
        unique_together = ['abandoned_vehicle', 'incident']


class NumberOfCartsAndPotholes(AutoCreatedUpdatedModel):
    """Model that contains number of carts for garbage carts incidents and number of potholes for potholes incidents.
    These are merged to one table because the data type is exactly the same.
    """
    number_of_elements = models.IntegerField()
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='number_of_carts_and_potholes')

    class Meta:
        db_table = 'number_of_carts_and_potholes'
        # Constraint to avoid duplication of data
        unique_together = ['number_of_elements', 'incident']


class Graffiti(AutoCreatedUpdatedModel):
    """Model that contains basic info about a graffiti
    """
    surface = models.CharField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'graffiti'  # The plural of graffiti is graffiti :)
        # Constraint to avoid duplication of data
        unique_together = ['surface', 'location']
        indexes = [models.Index(fields=['surface', 'location']), ]

    def clean(self):
        super().clean()
        if self.surface is None and self.location is None:
            raise ValidationError("Graffiti fields are all None")


class GraffitiIncident(AutoCreatedUpdatedModel):
    """Model that holds intermediate connection between graffiti and incidents
     """
    graffiti = models.ForeignKey(Graffiti, on_delete=models.CASCADE, related_name='graffiti_incidents')
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='graffiti_incidents')

    class Meta:
        db_table = 'graffiti_incidents'
        # Constraint to avoid duplication of data
        unique_together = ['graffiti', 'incident']


class Tree(AutoCreatedUpdatedModel):
    """Model that holds information about the location of tree events. This table is used for 'tree debris`
    & 'tree trims'
    """
    location = models.CharField(max_length=500, unique=True)

    class Meta:
        db_table = 'trees'
        indexes = [models.Index(fields=['location']), ]


class TreeIncident(AutoCreatedUpdatedModel):
    """Model that holds intermediate connection between graffiti and incidents
    """
    tree = models.ForeignKey(Tree, on_delete=models.CASCADE, related_name='tree_incidents')
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='tree_incidents')

    class Meta:
        db_table = 'tree_incidents'
        # Constraint to avoid duplication of data
        unique_together = ['tree', 'incident']


class RodentBaitingPremises(AutoCreatedUpdatedModel):
    """Model that holds information about the number of premises of a rodent baiting incident
    """
    number_of_premises_baited = models.IntegerField(null=True, blank=True)
    number_of_premises_w_garbage = models.IntegerField(null=True, blank=True)
    number_of_premises_w_rats = models.IntegerField(null=True, blank=True)
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='rodent_baiting_premises')

    class Meta:
        db_table = 'rodent_baiting_premises'
        # Constraint to avoid duplication of data
        unique_together = ['number_of_premises_baited', 'number_of_premises_w_garbage', 'number_of_premises_w_rats',
                           'incident']

    def clean(self):
        super().clean()
        if self.number_of_premises_baited is None and self.number_of_premises_w_garbage is None \
                and self.number_of_premises_w_rats is None:
            raise ValidationError("Rodent baiting premises fields are all None")


class SanitationCodeViolation(AutoCreatedUpdatedModel):
    """Model that holds the codes of violations
    """
    nature_of_code_violation = models.CharField(max_length=500, unique=True)

    class Meta:
        db_table = 'sanitation_code_violations'
        indexes = [models.Index(fields=['nature_of_code_violation']), ]


class SanitationCodeViolationIncident(AutoCreatedUpdatedModel):
    """Model that holds intermediate connection between sanitation code violations and incidents
    """
    sanitation_code_violation = models.ForeignKey(SanitationCodeViolation, on_delete=models.CASCADE,
                                                  related_name='sanitation_code_violations_incidents')
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE,
                                 related_name='sanitation_code_violations_incidents')

    class Meta:
        db_table = 'sanitation_code_violations_incidents'
        # Constraint to avoid duplication of data
        unique_together = ['sanitation_code_violation', 'incident']
