import axios from 'axios'
import authHeader from "@/services/auth-header";

const API_URL = 'http://localhost:8000/api/v1/';

class CreateIncidentService {

    _prepare_incident_data(incident) {
        let cr_date;
        let cm_date;
        if (incident.creation_date) {
            cr_date = new Date(incident.creation_date);
            cr_date = cr_date.toISOString();
        } else
            cr_date = null;
        if (incident.completion_date) {
            cm_date = new Date(incident.completion_date);
            cm_date = cm_date.toISOString();
        } else {
            cm_date = null;
        }
        return {
            creation_date: cr_date,
            completion_date: cm_date,
            status: incident.status,
            service_request_number: incident.service_request_number,
            type_of_service_request: incident.type_of_service_request,
            street_address: incident.street_address,
            zip_code: incident.zip_code,
            zip_codes: parseInt(incident.zip_codes),
            x_coordinate: parseFloat(incident.x_coordinate),
            y_coordinate: parseFloat(incident.y_coordinate),
            latitude: parseFloat(incident.latitude),
            longitude: parseFloat(incident.longitude),
            ward: parseInt(incident.ward),
            wards: parseInt(incident.wards),
            historical_wards_03_15: parseInt(incident.historical_wards_03_15),
            police_district: parseInt(incident.police_district),
            community_area: parseInt(incident.community_area),
            community_areas: parseInt(incident.community_areas),
            ssa: parseInt(incident.ssa),
            census_tracts: parseInt(incident.census_tracts)
        }
    }

    incident(incident) {
        const data = this._prepare_incident_data(incident)
        return axios
            .post(API_URL + 'incidents/', data, {headers: authHeader()})
    }

}

export default new CreateIncidentService();
