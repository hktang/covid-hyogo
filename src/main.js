import Vue from "vue";
import App from "./App.vue";
import "leaflet/dist/leaflet.css";
import "vue-loading-overlay/dist/vue-loading.css";
import * as Sentry from "@sentry/browser";
import * as Integrations from "@sentry/integrations";

Vue.config.productionTip = false;

new Vue({
  render: h => h(App)
}).$mount("#app");

Sentry.init({
  dsn: "https://534d3fcaa0da4806a747945b80051083@sentry.io/4771975",
  integrations: [new Integrations.Vue({ Vue, attachProps: true })]
});
