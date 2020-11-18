import axios from 'axios';
import authHeader from './auth-header';

const API_URL = 'http://localhost:8000/api/v1/';

class UserService {
    getUserInfo() {
        return axios.get(API_URL + 'users/', { headers: authHeader() });
    }
}

export default new UserService();
