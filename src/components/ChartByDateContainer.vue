<template>
  <div class="container">
    <h2>Daily new confirmed cases</h2>
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
          let dailyF=[]
          let dailyM=[]
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
            switch(responseData.feed.entry[i]['title']['$t'].substring(0,1)){
              case "B":
                if (!excludedRowIds.includes(responseData.feed.entry[i]['title']['$t'].substring(1))){
                  dailyF.push(responseData.feed.entry[i]['content']['$t'])
                }
                break
              case "C":
                if (!excludedRowIds.includes(responseData.feed.entry[i]['title']['$t'].substring(1))){
                  dailyM.push(responseData.feed.entry[i]['content']['$t'])
                }
                break
              default:
                break
            }
          }
          this.chartdata = {
            labels: dateLabels,
            datasets: [
              {
                label: 'Female',
                backgroundColor: '#42b983',
                //data: dailyConfirmed,
                data: dailyF,
              },
              {
                label: 'Male',
                backgroundColor: '#423383',
                //data: dailyConfirmed,
                data: dailyM,
              }
            ]
          }
          this.options = {        
            maintainAspectRatio: false,
            responsive: true,
            scales: {
              xAxes: [{
                  stacked: true
              }],
              yAxes: [{
                  ticks: {
                      beginAtZero: true
                  },
                  stacked: true
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
@media only screen and (max-width: 800px) {
  .chart {
    width: 90vw;
    height: 300px;
    margin: 0 auto;
  }
}

@media only screen and (min-width: 800px) {
  .chart {
    width: 50vw;
    height: 50vh;
    margin: 0 auto;
  }
}

</style>