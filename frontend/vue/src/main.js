import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import VueKatex from 'vue-katex'
import "katex/dist/katex.min.css";
import VueCarousel from 'vue-carousel';

Vue.config.productionTip = false
Vue.use(VueKatex)
Vue.use(VueCarousel)
new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
