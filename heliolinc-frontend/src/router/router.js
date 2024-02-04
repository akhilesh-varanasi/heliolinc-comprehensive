import { createRouter, createWebHistory } from 'vue-router';

import HomePage from '../components/HomePage.vue'
import LoginPage from '../components/LoginPage.vue'

const routes = [
    {
        path: '/',
        component: HomePage,
    },
    {
        path: '/login/',
        component: LoginPage
    }
]

export default function (){
    return createRouter({
        history: createWebHistory(),
        routes
    })
} 