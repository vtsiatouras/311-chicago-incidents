import axios from 'axios';
import authHeader from './auth-header';
import jwt_decode from "jwt-decode";

const API_URL = 'http://localhost:8000/api/v1/';

class UserService {
    getUserInfoFromAPI() {
        return axios.get(API_URL + 'users/', { headers: authHeader() });
    }

    getUserInfoFromToken() {
        try {
            let user = JSON.parse(localStorage.getItem('user'));
            const decoded = jwt_decode(user.access)
            return [decoded.user_id, decoded.user_name, decoded.user_email]
        } catch (error) {
            return [null, null, null]
        }
    }
}

export default new UserService();
