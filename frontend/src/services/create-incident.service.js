import axios from 'axios'
import authHeader from "@/services/auth-header";

const API_URL = 'http://localhost:8000/api/v1/';

class CreateIncidentService {

    _prepareIncidentData(incident) {
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
            creation_date: cr_date || null,
            completion_date: cm_date || null,
            status: incident.status || null,
            service_request_number: incident.service_request_number || null,
            type_of_service_request: incident.type_of_service_request || null,
            street_address: incident.street_address || null,
            zip_code: incident.zip_code || null,
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

    _prepareIncidentActivityData(activity) {
        if (activity.current_activity || activity.most_recent_action) {
            return {
                current_activity: activity.current_activity || null,
                most_recent_action: activity.most_recent_action || null
            };
        } else {
            return null;
        }

    }

    _prepareAbandonedVehicleData(vehicle) {
        if (vehicle.license_plate || vehicle.vehicle_make_model || vehicle.vehicle_color) {
            return {
                license_plate: vehicle.license_plate || null,
                vehicle_make_model: vehicle.vehicle_make_model || null,
                vehicle_color: vehicle.vehicle_color || null
            };
        } else {
            return null;
        }
    }

    _prepareGarbageCartsPotholesData(garbageCartPorthole) {
        if (garbageCartPorthole.number_of_elements) {
            return {
                number_of_elements:  parseInt(garbageCartPorthole.number_of_elements)
            };
        } else {
            return null;
        }
    }

    _prepareGraffitiData(graffiti) {
        if (graffiti.surface || graffiti.location) {
            return {
                surface :graffiti.surface || null,
                location: graffiti.location || null
            };
        } else {
            return null;
        }
    }

    _prepareRodentBaitingData(rodentBaiting) {
        console.log(rodentBaiting)
        if (rodentBaiting.number_of_premises_baited || rodentBaiting.number_of_premises_w_garbage ||
            rodentBaiting.number_of_premises_w_rats) {

            return {
                number_of_premises_baited:  parseInt(rodentBaiting.number_of_premises_baited),
                number_of_premises_w_garbage:  parseInt(rodentBaiting.number_of_premises_w_garbage),
                number_of_premises_w_rats:  parseInt(rodentBaiting.number_of_premises_w_rats)
            };
        } else {
            return null;
        }
    }

    _prepareSanitationCodeData(codeViolation) {
        if (codeViolation.nature_of_code_violation) {
            return {
                nature_of_code_violation: codeViolation.nature_of_code_violation || null
            };
        } else {
            return null;
        }
    }

    _prepareTreeData(tree) {
        if (tree) {
            return {
                location: tree.location || null
            };
        } else {
            return null;
        }
    }

    incident(incident) {
        const data = this._prepareIncidentData(incident);
        return axios
            .post(API_URL + 'incidents/', data, { headers: authHeader() })
    }

    abandonedVehicleIncident(incident, activity, vehicle, days_of_report_as_parked) {
        const incidentData = this._prepareIncidentData(incident);
        const activityData = this._prepareIncidentActivityData(activity);
        const vehicleData = this._prepareAbandonedVehicleData(vehicle);
        const data = {};
        data['incident'] = incidentData;
        if (activityData) {
            data['activity'] = activityData;
        }
        if (vehicleData) {
            data['abandoned_vehicle'] = vehicleData;
        }
        data['days_of_report_as_parked'] = parseInt(days_of_report_as_parked)
        return axios
            .post(API_URL + 'incidents/createAbandonedVehicleIncidents/', data, { headers: authHeader() })
    }

    garbageCartsPotholesIncident(incident, activity, garbageCartPorthole) {
        const incidentData = this._prepareIncidentData(incident);
        const activityData = this._prepareIncidentActivityData(activity);
        const garbageCartPortholeData = this._prepareGarbageCartsPotholesData(garbageCartPorthole);
        const data = {};
        data['incident'] = incidentData;
        if (activityData) {
            data['activity'] = activityData;
        }
        if (garbageCartPortholeData) {
            data['carts_and_potholes'] = garbageCartPortholeData;
        }
        return axios
            .post(API_URL + 'incidents/createGarbageCartsAndPotholesIncidents/', data, { headers: authHeader() })
    }

    graffitiIncident(incident, graffiti) {
        const incidentData = this._prepareIncidentData(incident);
        const graffitiData = this._prepareGraffitiData(graffiti);
        const data = {};
        data['incident'] = incidentData;
        if (graffitiData) {
            data['graffiti'] = graffitiData;
        }
        return axios
            .post(API_URL + 'incidents/createGraffitiIncidents/', data, { headers: authHeader() })

    }

    rodentBaitingIncident(incident, activity, rodentBaiting) {
        const incidentData = this._prepareIncidentData(incident);
        const activityData = this._prepareIncidentActivityData(activity);
        const rodentBaitingData = this._prepareRodentBaitingData(rodentBaiting);
        const data = {};
        data['incident'] = incidentData;
        if (activityData) {
            data['activity'] = activityData;
        }
        if (rodentBaitingData) {
            data['rodent_baiting_premises'] = rodentBaitingData;
        }
        console.log(data)
        return axios
            .post(API_URL + 'incidents/createRodentBaitingIncidents/', data, { headers: authHeader() })
    }

    sanitationCodeIncident(incident, sanitationCode) {
        const incidentData = this._prepareIncidentData(incident);
        const sanitationCodeData = this._prepareSanitationCodeData(sanitationCode);
        const data = {};
        data['incident'] = incidentData;
        if (sanitationCodeData) {
            data['sanitation_code_violation'] = sanitationCodeData;
        }
        return axios
            .post(API_URL + 'incidents/createSanitationCodeViolationIncidents/', data, { headers: authHeader() })
    }

    treeIncident(incident, activity, tree) {
        const incidentData = this._prepareIncidentData(incident);
        const activityData = this._prepareIncidentActivityData(activity);
        const treeData = this._prepareTreeData(tree);
        const data = {};
        data['incident'] = incidentData;
        if (activityData) {
            data['activity'] = activityData;
        }
        if (treeData) {
            data['tree'] = treeData;
        }
        return axios
            .post(API_URL + 'incidents/createTreeIncidents/', data, { headers: authHeader() })
    }

}

export default new CreateIncidentService();
