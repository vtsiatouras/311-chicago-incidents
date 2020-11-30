import Vue from 'vue';
import Router from 'vue-router';
import Home from './components/Home.vue';
import Login from './components/Login.vue';
import Register from './components/Register.vue';

Vue.use(Router);

export const router = new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'home',
            component: Home
        },
        {
            path: '/home',
            component: Home
        },
        {
            path: '/login',
            component: Login
        },
        {
            path: '/register',
            component: Register
        },
        {
            path: '/profile',
            name: 'profile',
            // lazy-loaded
            component: () => import('./components/Profile.vue')
        },
        {
            path: '/create-incident',
            name: 'create-incident',
            // lazy-loaded
            component: () => import('./components/IncidentCreate.vue')
        },
        {
            path: '/total-requests-per-type',
            name: 'total-requests-per-type',
            // lazy-loaded
            component: () => import('./components/queries/TotalRequestsPerType')
        },
        {
            path: '/total-requests-per-day',
            name: 'total-requests-per-day',
            // lazy-loaded
            component: () => import('./components/queries/TotalRequestsPerDay')
        },
        {
            path: '/most-common-service-per-zipcode',
            name: 'most-common-service-per-zipcode',
            // lazy-loaded
            component: () => import('./components/queries/MostCommonServicePerZipcode')
        },
        {
            path: '/average-completion-time-per-request',
            name: 'average-completion-time-per-request',
            // lazy-loaded
            component: () => import('./components/queries/AverageCompletionTimePerRequest')
        },
        {
            path: '/most-common-service-in-bounding-box',
            name: 'most-common-service-in-bounding-box',
            // lazy-loaded
            component: () => import('./components/queries/MostCommonServiceInBoundingBox')
        }
    ]
});

router.beforeEach((to, from, next) => {
    const publicPages = ['/login', '/register'];
    const authRequired = !publicPages.includes(to.path);
    const loggedIn = localStorage.getItem('user');

    // trying to access a restricted page + not logged in
    // redirect to login page
    if (authRequired && !loggedIn) {
        next('/login');
    } else {
        next();
    }
});
