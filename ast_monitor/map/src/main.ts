import './assets/main.css';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'leaflet/dist/leaflet.css';


import { createApp } from 'vue';
import { createPinia } from 'pinia';

import { OhVueIcon, addIcons } from "oh-vue-icons";
import { FaFlagCheckered, FaMountain } from "oh-vue-icons/icons";
addIcons(FaFlagCheckered, FaMountain);


import App from './App.vue';



const app = createApp(App);

app.use(createPinia());
app.component("v-icon", OhVueIcon);

app.mount('#app');
