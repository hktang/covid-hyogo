<template>
  <div id="app">
    <LocaleSwitch />
    <img alt="Hyogo logo" src="./assets/hyogo.svg" />
    <h1 class="site-title">{{ $t("siteURL") }}</h1>
    <p class="muted">{{ $t("siteTagline") }}</p>
    <Summary />
    <div class="chart-by-date">
      <ChartByDateContainer />
    </div>
    <ChartByStatusContainer />
    <ChartByClusterContainer />
    <ChartByAgeContainer />
    <MapByCity />
    <Footer />
  </div>
</template>
<script>
import LocaleSwitch from "./components/LocaleSwitch.vue";
import Summary from "./components/Summary.vue";
import ChartByDateContainer from "./components/ChartByDateContainer.vue";
import ChartByClusterContainer from "./components/ChartByClusterContainer.vue";
import ChartByStatusContainer from "./components/ChartByStatusContainer.vue";
import ChartByAgeContainer from "./components/ChartByAgeContainer.vue";
import MapByCity from "./components/MapByCity.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "App",
  components: {
    LocaleSwitch,
    Summary,
    ChartByDateContainer,
    ChartByClusterContainer,
    ChartByStatusContainer,
    ChartByAgeContainer,
    MapByCity,
    Footer
  }
};
</script>

<style>
body {
  margin-top: 0;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0;
  padding-top: 0;
}
.site-title {
  font-size: 1.5em;
  text-transform: uppercase;
}
.muted {
  color: #aaa;
  margin-bottom: 20px;
  font-size: 15px;
}
.footer {
  padding-bottom: 40px;
}
.chart-by-date {
  min-height: 50vh;
}
</style>
