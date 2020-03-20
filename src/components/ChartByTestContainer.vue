<template>
  <div class="container">
    <h2>Patient status (accumulative)</h2>
    <loading :active.sync="loading"></loading>
    <chart-by-test
      v-if="loaded"
      class="chart"
      :chartdata="chartdata"
      :options="options"
    />
  </div>
</template>

<script>
import axios from "axios";
import ChartByTest from "./BarChart.vue";
import Loading from "vue-loading-overlay";

export default {
  name: "ChartByDateContainer",
  components: { ChartByTest, Loading },
  data: () => ({
    loading: true,
    loaded: false,
    chartdata: null
  }),
  async mounted() {
    this.getData();
  },
  methods: {
    getData: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/" +
            "1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw" +
            "/5/public/basic?alt=json"
        )
        .then(response => {
          const responseData = response.data;
          let dateLabels = [];
          let totalPositive = [];
          let nonCritical = [];
          let critical = [];
          let deaths = [];

          const entries = responseData.feed.entry;

          for (let i = 0; i < entries.length; i++) {
            if (entries[i]["title"]["$t"].substring(0, 1) == "A") {
              if (!isNaN(entries[i]["content"]["$t"].substring(0, 4))) {
                dateLabels.push(entries[i]["content"]["$t"]);
              }
            }
          }

          const totalPositiveCases = entries.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) == "C";
          });
          totalPositive = totalPositiveCases.map(c => c["content"]["$t"]);
          totalPositive.shift();

          const nonCriticalCases = entries.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) == "E";
          });
          nonCritical = nonCriticalCases.map(c => c["content"]["$t"]);
          nonCritical.shift();

          const criticalCases = entries.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) == "F";
          });
          critical = criticalCases.map(c => c["content"]["$t"]);
          critical.shift();

          const deathCases = entries.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) == "G";
          });
          deaths = deathCases.map(c => c["content"]["$t"]);
          deaths.shift();

          this.chartdata = {
            labels: dateLabels,
            datasets: [
              {
                label: "Non-critical",
                backgroundColor: "#42b983",
                data: nonCritical
              },
              {
                label: "Critical",
                backgroundColor: "#194531",
                data: critical
              },
              {
                label: "Deaths",
                backgroundColor: "#7c7f7e",
                data: deaths
              },
              {
                label: "Accumulated confirmed",
                backgroundColor: "#c2ead7",
                borderColor: "#42b983",
                borderWidth: 1,
                data: totalPositive,
                type: "line"
              }
            ]
          };

          this.options = {
            maintainAspectRatio: false,
            responsive: true,
            elements: {
              point: {
                radius: 0
              }
            },
            scales: {
              xAxes: [
                {
                  stacked: true,
                  ticks: {
                    reverse: true
                  }
                }
              ],
              yAxes: [
                {
                  stacked: true,
                  ticks: {
                    beginAtZero: true
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
    }
  }
};
</script>

<style scoped>
.container {
  margin: 20px auto;
  padding: 20px 0 50px;
  background-color: #fafafa;
}

.chart {
  padding: 0;
  margin: 0 auto;
}

@media only screen and (max-width: 800px) {
  .container {
    min-height: 300px;
  }

  .chart {
    width: 90vw;
    height: 300px;
  }
}

@media only screen and (min-width: 800px) {
  .container {
    min-height: 50vh;
  }

  .chart {
    width: 50vw;
    height: 50vh;
  }
}
</style>
