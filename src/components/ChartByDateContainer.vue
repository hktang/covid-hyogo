<template>
  <div class="container">
    <chart-by-date
      class="chart"
      v-if="loaded"
      :chartdata="chartdata"
      :options="options"/>
  </div>
</template>

<script>
import ChartByDate from './ChartByDate.vue'
import axios from 'axios'

export default {
  name: 'ChartByDateContainer',
  components: { ChartByDate },
  data: () => ({
    loaded: false,
    chartdata: null
  }),
  async mounted () {
    this.loaded = false
    this.getData()
  },
  methods: {
    getData: function() {
      axios.get('https://spreadsheets.google.com/feeds/cells/1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw/2/public/basic?alt=json')
        .then(response => {
          const responseData = response.data

          let dateLabels = []
          let excludedRowIds = []
          let dailyConfirmed=[]
          for (let i=0; i<responseData.feed.entry.length; i++){
            if(responseData.feed.entry[i]['title']['$t'].substring(0,1) == "A"){
              if (responseData.feed.entry[i]['content']['$t'].substring(0,4) == "2020"){
                dateLabels.push(responseData.feed.entry[i]['content']['$t'])
              }else{
                excludedRowIds.push(responseData.feed.entry[i]['title']['$t'].substring(1))
              }
            }
          }
          console.log(excludedRowIds)
          for (let i=0; i<responseData.feed.entry.length; i++){
            if(responseData.feed.entry[i]['title']['$t'].substring(0,1) == "D"){
              if (!excludedRowIds.includes(responseData.feed.entry[i]['title']['$t'].substring(1))){
                dailyConfirmed.push(responseData.feed.entry[i]['content']['$t'])
              }
            }
          }
          this.chartdata = {
            labels: dateLabels,
            datasets: [
              {
                label: 'Daily confirmed cases',
                backgroundColor: '#42b983',
                data: dailyConfirmed,
              }
            ]
          }
          this.options = {        
            maintainAspectRatio: false,
            responsive: true,
            scales: {
              yAxes: [{
                  ticks: {
                      beginAtZero: true
                  }
              }]
            }
          }
          this.loaded = true
        }).catch(error => {
          console.log(error)
      });
    }
  }
}
</script>

<style>
.chart {
  width: 75vw;
  height: 50vh;
  margin: 0 auto;
}
</style>