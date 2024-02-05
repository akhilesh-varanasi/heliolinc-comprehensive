import { getAuth, onAuthStateChanged } from 'firebase/auth';
import { createRouter, createWebHistory } from 'vue-router';

import HomePage from '../components/HomePage.vue'
import LoginPage from '../components/LoginPage.vue'
import LoginRegisterPage from '../components/LoginRegister.vue'
import RegisterPage from '../components/RegisterPage.vue'
const routes = [
    {
        path: '/',
        component: LoginRegisterPage
    },
    {
        path: '/login2/',
        component: LoginPage
    },
    {
        path: '/register/',
        component: RegisterPage
    },
    {
        path: '/login/',
        component: LoginRegisterPage
    },
    {
        path: '/home/',
        component: HomePage,
        meta: {
            requiresAuth: true,
        },
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
});

const getCurrentUser = () => {
    return new Promise((resolve, reject) => {
        const removeListener = onAuthStateChanged(
            getAuth(),
            (user) => {
                removeListener();
                resolve(user)
            },
            reject
        );
    });
}

router.beforeEach(async(to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresAuth)) {
        if (await getCurrentUser()) {
            next();
        } else {
            alert("you don't have access :)");
            next("/");
        }
    } else {
        next();
    }
});

export default router;