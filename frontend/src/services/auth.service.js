import axios from 'axios';

const API_URL = 'http://localhost:8000/api/v1/';

class AuthService {
    login(user) {
        return axios
            .post(API_URL + 'auth/', {
                username: user.username,
                password: user.password
            })
            .then(response => {
                if (response.data.access) {
                    localStorage.setItem('user', JSON.stringify(response.data));
                }

                return response.data;
            });
    }

    logout() {
        localStorage.removeItem('user');
    }

    getNewToken() {
        let user = JSON.parse(localStorage.getItem('user'));
        return new Promise((resolve, reject) => {
            axios
                .post(API_URL + 'auth/refresh/', { refresh: user.refresh })
                .then(response => {
                    user['access'] = response.data['access']
                    localStorage.setItem("user", JSON.stringify(user));
                    resolve(response.data.access);
                })
                .catch((error) => {
                    reject(error);
                });
        });
    }

    register(user) {
        return axios.post(API_URL + 'users', {
            username: user.username,
            email: user.email,
            password: user.password
        });
    }
}

export default new AuthService();
