export default class Incident {
    constructor(creation_date, completion_date, status, service_request_number, type_of_service_request,
        street_address, zip_code, zip_codes, x_coordinate, y_coordinate, latitude, longitude,
        ward, wards, historical_wards_03_15, police_district, community_area, community_areas, ssa,
        census_tracts) {
        this.creation_date = creation_date;
        this.completion_date = completion_date;
        this.status = status;
        this.service_request_number = service_request_number;
        this.type_of_service_request = type_of_service_request;
        this.street_address = street_address;
        this.zip_code = zip_code;
        this.zip_codes = zip_codes;
        this.x_coordinate = x_coordinate;
        this.y_coordinate = y_coordinate;
        this.latitude = latitude;
        this.longitude = longitude;
        this.ward = ward;
        this.wards = wards;
        this.historical_wards_03_15 = historical_wards_03_15;
        this.police_district = police_district;
        this.community_area = community_area;
        this.community_areas = community_areas;
        this.ssa = ssa;
        this.census_tracts = census_tracts;
    }
}
