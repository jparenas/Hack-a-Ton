import Vue from 'vue'

import router from './router'

import BootstrapVue from 'bootstrap-vue'
import UUID from 'vue-uuid';

import App from './App'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(BootstrapVue);
Vue.use(UUID);

Vue.config.productionTip = false;

new Vue({
  el: '#app',
  router,
  template: '<App/>',
  components: {
    App
  }
})
