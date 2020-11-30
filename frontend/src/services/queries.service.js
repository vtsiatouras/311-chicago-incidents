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

    averageCompletionTimePerRequest(startDate, endDate) {
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
            .get(API_URL + 'queries/averageCompletionTimePerRequest/', {params: params, headers: authHeader()});
    }

    mostCommonServiceInBoundingBox(date, a_latitude, a_longitude, b_latitude, b_longitude) {
        const dateData = this._prepareDate(date);
        const params = new URLSearchParams();
        if (dateData) {
            params.append('date', dateData);
        }
        params.append('a_latitude', parseFloat(a_latitude).toString())
        params.append('a_longitude', parseFloat(a_longitude).toString())
        params.append('b_latitude', parseFloat(b_latitude).toString())
        params.append('b_longitude', parseFloat(b_longitude).toString())
        return axios
            .get(API_URL + 'queries/mostCommonServiceInBoundingBox/', {params: params, headers: authHeader()});
    }

    top5SSA(startDate, endDate) {
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
            .get(API_URL + 'queries/top5SSA/', {params: params, headers: authHeader()});
    }

    licensePlates() {
        return axios
            .get(API_URL + 'queries/licensePlates/', {headers: authHeader()});
    }

    secondMostCommonColor() {
        return axios
            .get(API_URL + 'queries/secondMostCommonColor/', {headers: authHeader()});
    }

    rodentBaiting(page, threshold, typeOfPremises) {
        const params = new URLSearchParams();
        params.append('page', parseInt(page).toString())
        params.append('threshold', parseInt(threshold).toString())
        params.append('type_of_premises', typeOfPremises);
        return axios
            .get(API_URL + 'queries/rodentBaiting/', {params: params, headers: authHeader()});
    }
}

export default new QueriesService();
