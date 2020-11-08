from django.db import models


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
    current_activity = models.CharField(max_length=100, null=True, blank=True)
    most_recent_action = models.CharField(max_length=100, null=True, blank=True)
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
        # The 1st index is useful for the importers
        indexes = [models.Index(fields=['creation_date', 'status', 'completion_date', 'service_request_number',
                                        'type_of_service_request', 'street_address'])]

    def __str__(self):
        """Return the string representation of the incident.

        :return: The service request number.
        """
        return self.service_request_number


class AbandonedVehicle(AutoCreatedUpdatedModel):
    """Model for abandoned cars
    """
    license_plate = models.CharField(max_length=400)
    vehicle_make_model = models.CharField(max_length=100, null=True, blank=True)
    vehicle_color = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'abandoned_vehicles'
        unique_together = ['license_plate', 'vehicle_make_model', 'vehicle_color']
        # The 1st index is useful for the importers
        indexes = [models.Index(fields=['license_plate', 'vehicle_make_model', 'vehicle_color'])]

    def __str__(self):
        """Return the string representation of the incident.

        :return: The service request number.
        """
        return self.license_plate


class AbandonedVehicleIncident(AutoCreatedUpdatedModel):
    """Model that holds information about abandoned cars. In that way we can hold one to many relations and more
    precisely a car can belong to multiple incidents (also it is supported many to many too, one incident can have
    multiple cars but this is not required)
    """
    abandoned_vehicle = models.ForeignKey(AbandonedVehicle, on_delete=models.CASCADE,
                                          related_name='abandoned_vehicles_incidents')
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='abandoned_vehicles_incidents')
    days_of_report_as_parked = models.BigIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'abandoned_vehicles_incidents'
        unique_together = ['abandoned_vehicle', 'incident']


class NumberOfCartsAndPotholes(AutoCreatedUpdatedModel):
    """Model that contains number of carts for garbage carts incidents and number of potholes for potholes incidents.
    These are merged to one table because the data type is exactly the same.
    """
    number_of_elements = models.IntegerField()
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='number_of_carts_and_potholes')

    class Meta:
        db_table = 'number_of_carts_and_potholes'


class Graffiti(AutoCreatedUpdatedModel):
    """Model that contains basic info about a graffiti
    """
    surface = models.CharField(max_length=500)
    location = models.CharField(max_length=500)

    class Meta:
        db_table = 'graffiti'   # The plural of graffiti is graffiti :)


class GraffitiIncident(AutoCreatedUpdatedModel):
    """Model that holds intermediate connection between graffiti and incidents
     """
    graffiti = models.ForeignKey(Graffiti, on_delete=models.CASCADE, related_name='graffiti_incidents')
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='graffiti_incidents')

    class Meta:
        db_table = 'graffiti_incidents'


class Tree(AutoCreatedUpdatedModel):
    """Model that holds information about the location of tree events. This table is used for 'tree debris`
    & 'tree trims'
    """
    location = models.CharField(max_length=500)

    class Meta:
        db_table = 'trees'


class TreeIncident(AutoCreatedUpdatedModel):
    """Model that holds intermediate connection between graffiti and incidents
    """
    graffiti = models.ForeignKey(Graffiti, on_delete=models.CASCADE, related_name='tree_incidents')
    incident = models.ForeignKey(Incident, on_delete=models.CASCADE, related_name='tree_incidents')

    class Meta:
        db_table = 'tree_incidents'
