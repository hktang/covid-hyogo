<template>
  <div id="app">
    <h1>COVID-19 Hyogo</h1>
    <ChartByDateContainer/>
    <ChartByCity/>
  </div>
</template>

<script>
import ChartByDateContainer from './components/ChartByDateContainer.vue'
import ChartByCity from './components/ChartByCity.vue'

export default {
  name: 'App',
  components: {
    ChartByDateContainer,
    ChartByCity
  }
}
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
