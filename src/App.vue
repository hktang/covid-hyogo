<template>
  <div id="app">
    <h1>COVID-19 Hyogo</h1>
    <ChartByDateContainer />
    <MapByCity />
    <div class="footer">
      <h2>Primary data source</h2>
      <p>
        Data from
        <a href="https://web.pref.hyogo.lg.jp/kk03/corona_hasseijyokyo.html">
          新型コロナウイルスに感染した患者の発生状況</a
        >, Hyogo Prefectural Government
      </p>
      <p>
        Available as
        <a
          href="https://docs.google.com/spreadsheets/d/e/2PACX-1vTM9vP7fGowD3SKSGDGpIWBpbGHLclWW2TmbGyejLM5e3h9CwWvz9sP8a7I0C-F98bL6L-grr7bF6X5/pubhtml"
        >
          Google Spreadsheet</a
        >
      </p>
    </div>
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
.footer {
  padding-bottom: 40px;
}
</style>
