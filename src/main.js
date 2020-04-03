import Vue from "vue";
import App from "./App.vue";
import * as Sentry from "@sentry/browser";
import VueGtag from "vue-gtag";
import VueMeta from 'vue-meta'
import * as Integrations from "@sentry/integrations";
import "vue-loading-overlay/dist/vue-loading.css";
import "leaflet/dist/leaflet.css";
import i18n from "./i18n";
Vue.config.productionTip = false;
Vue.use(require("vue-moment"));
Vue.use(VueMeta)

new Vue({
  i18n,
  render: h => h(App)
}).$mount("#app");

Vue.use(VueGtag, {
  config: { id: "UA-160715980-1" }
});

Sentry.init({
  dsn: "https://534d3fcaa0da4806a747945b80051083@sentry.io/4771975",
  integrations: [new Integrations.Vue({ Vue, attachProps: true })]
});
