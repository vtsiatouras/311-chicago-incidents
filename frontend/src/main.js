import Vue from 'vue';
import App from './App.vue';
import { router } from './router';
import store from './store';
import 'bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css'
import BootstrapVue from 'bootstrap-vue';
import VeeValidate from 'vee-validate';
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import {
    faHome,
    faUser,
    faUserPlus,
    faSignInAlt,
    faSignOutAlt
} from '@fortawesome/free-solid-svg-icons';
import axios from 'axios';
import AuthService from './services/auth.service'

library.add(faHome, faUser, faUserPlus, faSignInAlt, faSignOutAlt);

Vue.config.productionTip = false;

Vue.use(VeeValidate);
Vue.use(BootstrapVue);
Vue.component('font-awesome-icon', FontAwesomeIcon);

axios.interceptors.response.use((response) => {
    // Return a successful response back to the calling service
    return response;
}, (error) => {
    // Return any error which is not due to authentication back to the calling service
    if (error.response.status !== 403) {
        return new Promise((resolve, reject) => {
            reject(error);
        });
    }

    // Logout user if token refresh didn't work or user is disabled
    if (error.config.url == '/api/auth/refresh' || error.response.message == 'Account is disabled.') {

        AuthService.logout();
        router.push('login');

        return new Promise((resolve, reject) => {
            reject(error);
        });
    }

    // Try request again with new token
    return AuthService.getNewToken()
        .then((token) => {

            // New request with new token
            const config = error.config;
            config.headers['Authorization'] = `Bearer ${token}`;

            return new Promise((resolve, reject) => {
                axios.request(config).then(response => {
                    resolve(response);
                }).catch((error) => {
                    reject(error);
                })
            });

        })
        .catch((error) => {
            Promise.reject(error);
        });
});


new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app');
