<template>
  <div id="app">
    <img alt="Hyogo logo" src="./assets/hyogo.svg" />
    <h1>{{ $t("siteTitle") }}</h1>
    <p class="muted">{{ $t("siteTagline") }}</p>
    <div class="chart-by-date">
      <ChartByDateContainer />
    </div>
    <ChartByClusterContainer />
    <ChartByStatusContainer />
    <ChartByAgeContainer />
    <MapByCity />
    <Footer />
  </div>
</template>

<script>
import ChartByAgeContainer from "./components/ChartByAgeContainer.vue";
import ChartByDateContainer from "./components/ChartByDateContainer.vue";
import ChartByClusterContainer from "./components/ChartByClusterContainer.vue";
import ChartByStatusContainer from "./components/ChartByStatusContainer.vue";
import MapByCity from "./components/MapByCity.vue";
import Footer from "./components/Footer.vue";

export default {
  name: "App",
  components: {
    ChartByAgeContainer,
    ChartByDateContainer,
    ChartByClusterContainer,
    ChartByStatusContainer,
    MapByCity,
    Footer
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 40px;
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
