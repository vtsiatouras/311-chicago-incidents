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
        };
    }

    _prepare_incident_activity_data(activity) {
        if (activity.current_activity && activity.most_recent_action) {
            return {
                current_activity: activity.current_activity,
                most_recent_action: activity.most_recent_action
            };
        } else {
            return null;
        }

    }

    _prepare_abandoned_vehicle_data(vehicle) {
        if (vehicle.license_plate && vehicle.vehicle_make_model && vehicle.vehicle_color) {
            return {
                license_plate: vehicle.license_plate,
                vehicle_make_model: vehicle.vehicle_make_model,
                vehicle_color: vehicle.vehicle_color
            };
        } else {
            return null;
        }
    }

    incident(incident) {
        const data = this._prepare_incident_data(incident);
        return axios
            .post(API_URL + 'incidents/', data, { headers: authHeader() })
    }

    abandonedVehicleIncident(incident, activity, vehicle) {
        const incident_data = this._prepare_incident_data(incident);
        const activity_data = this._prepare_incident_activity_data(activity);
        const vehicle_data = this._prepare_abandoned_vehicle_data(vehicle);
        const data = {};
        data['incident'] = incident_data;
        if (activity_data) {
            data['activity'] = activity_data;
        }
        if (vehicle_data) {
            data['abandoned_vehicle'] = vehicle_data;
        }
        return axios
            .post(API_URL + 'incidents/createAbandonedVehicleIncidents/', data, { headers: authHeader() })
    }

}

export default new CreateIncidentService();
