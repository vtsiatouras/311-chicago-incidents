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

}

export default new QueriesService();
