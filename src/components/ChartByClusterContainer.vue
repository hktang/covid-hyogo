<template>
  <div class="container">
    <h2>Clusters</h2>
    <loading :active.sync="loading"></loading>
    <chart-by-cluster
      v-if="loaded"
      class="chart"
      :chartdata="chartdata"
      :options="options"
    />
  </div>
</template>

<script>
import axios from "axios";
import ChartByCluster from "./ScatterPlot.vue";

export default {
  name: "ChartByDateContainer",
  components: { ChartByCluster },
  data: () => ({
    loaded: false,
    chartdata: null,
    xMap: ["", "Kindergarten", "Livehouse", "Hospital", ""],
    yMap: ["", "January", "February", "March", "April", "May", "June", "July"]
  }),
  async mounted() {
    this.getData();
  },
  methods: {
    getData: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw/4/public/basic?alt=json"
        )
        .then(response => {
          const responseData = response.data;
          console.log(responseData);
          this.chartdata = {
            datasets: [
              {
                label: "My First dataset",
                data: [
                  this.mapDataPoint("Kindergarten", "January"),
                  this.mapDataPoint("Livehouse", "February"),
                  this.mapDataPoint("Hospital", "February"),
                  this.mapDataPoint("Kindergarten", "March"),
                  this.mapDataPoint("Hospital", "March")
                ],
                fill: false,
                showLine: false,
                pointRadius: 10,
                borderColor: "#acacac",
                backgroundColor: "#cacaca"
              }
            ]
          };
          this.options = {
            responsive: true,
            title: {
              display: false
            },
            legend: {
              display: false
            },
            scales: {
              xAxes: [
                {
                  type: "linear",
                  position: "top",
                  scaleLabel: {
                    display: false
                  },
                  ticks: {
                    min: 0,
                    max: this.xMap.length - 1,
                    callback: value => {
                      return this.xMap[value];
                    }
                  }
                }
              ],
              yAxes: [
                {
                  scaleLabel: {
                    display: false
                  },
                  ticks: {
                    reverse: true,
                    min: 0,
                    max: this.yMap.length - 1,
                    callback: value => {
                      return this.yMap[value];
                    }
                  }
                }
              ]
            }
          };
          this.loaded = true;
          this.loading = false;
        })
        .catch(error => {
          console.log(error);
        });
    },
    // Courtesy of https://stackoverflow.com/questions/43090102/chartjs-mapping-non-numeric-y-and-x
    mapDataPoint: function(xValue, yValue) {
      return {
        x: this.xMap.indexOf(xValue),
        y: this.yMap.indexOf(yValue)
      };
    }
  }
};
</script>

<style scoped>
.container {
}

.chart {
}

@media only screen and (max-width: 800px) {
}

@media only screen and (min-width: 800px) {
}
</style>
