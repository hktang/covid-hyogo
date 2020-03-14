<template>
  <div id="app">
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
</style>
