<template>
  <div id="app">
    <h1>COVID-19 Hyogo</h1>
    <ChartByDateContainer />
    <MapByCity />
  </div>
</template>

<script>
import ChartByDateContainer from "./components/ChartByDateContainer.vue";
import MapByCity from "./components/MapByCity.vue";

export default {
  name: "App",
  components: {
    ChartByDateContainer,
    MapByCity
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
  margin-top: 60px;
}
.muted {
  color: #333;
  margin-bottom: 40px;
}
</style>
