import axios from 'axios'
import authHeader from "@/services/auth-header";

const API_URL = 'http://localhost:8000/api/v1/';

class QueriesService {

    _prepareDate(dateString) {
        let date;
        if (dateString) {
            date = new Date(dateString);
            date = date.toISOString().split('T')[0];
        } else {
            date = null;
        }
        return date;
    }

    totalRequestsPerType(startDate, endDate) {
        const startDateData = this._prepareDate(startDate);
        const endDateData = this._prepareDate(endDate);
        const params = new URLSearchParams();
        if (startDateData) {
            params.append('start_date', startDateData);
        }
        if (endDateData) {
            params.append('end_date', endDateData);
        }
        return axios
            .get(API_URL + 'queries/totalRequestsPerType/', {params: params, headers: authHeader()});
    }

    totalRequestsPerDay(startDate, endDate, typeOfServiceRequest) {
        const startDateData = this._prepareDate(startDate);
        const endDateData = this._prepareDate(endDate);
        const params = new URLSearchParams();
        if (startDateData) {
            params.append('start_date', startDateData);
        }
        if (endDateData) {
            params.append('end_date', endDateData);
        }
        params.append('type_of_service_request', typeOfServiceRequest);
        return axios
            .get(API_URL + 'queries/totalRequestsPerDay/', {params: params, headers: authHeader()});
    }

    mostCommonServicePerZipcode(date) {
        const dateData = this._prepareDate(date);
        const params = new URLSearchParams();
        if (dateData) {
            params.append('date', dateData);
        }
        return axios
            .get(API_URL + 'queries/mostCommonServicePerZipcode/', {params: params, headers: authHeader()});
    }

}

export default new QueriesService();
