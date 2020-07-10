// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import axios from 'axios'
import VueAxios from 'vue-axios'
import App from './App'
import router from './router'
import qs from 'qs'
import Message from 'element-ui'
import locale from 'element-ui/lib/locale/lang/en'
// import 'bootstrap/dist/css/bootstrap.min.css'

Vue.prototype.$qs = qs;
Vue.config.productionTip = false


Vue.use(ElementUI, {locale});
Vue.use(VueAxios,axios);
Vue.use(qs);


/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
