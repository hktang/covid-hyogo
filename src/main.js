import Vue from "vue";
import App from "./App.vue";
import * as Sentry from "@sentry/browser";
import VueAnalytics from "vue-analytics";
import * as Integrations from "@sentry/integrations";
import "vue-loading-overlay/dist/vue-loading.css";
import "leaflet/dist/leaflet.css";
Vue.config.productionTip = false;

new Vue({
  render: h => h(App)
}).$mount("#app");

Vue.use(VueAnalytics, {
  id: "UA-160715980-1"
});

Sentry.init({
  dsn: "https://534d3fcaa0da4806a747945b80051083@sentry.io/4771975",
  integrations: [new Integrations.Vue({ Vue, attachProps: true })]
});
