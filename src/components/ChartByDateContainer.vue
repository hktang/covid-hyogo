<template>
  <div class="container">
    <h2>Daily new confirmed cases</h2>
    <p class="muted">
      Last updated: <br />
      {{ lastUpdated }}
    </p>
    <loading :active.sync="loading"></loading>
    <chart-by-date
      v-if="loaded"
      class="chart"
      :chartdata="chartdata"
      :options="options"
    />
  </div>
</template>

<script>
import axios from "axios";
import ChartByDate from "./ChartByDate.vue";
import Loading from "vue-loading-overlay";

export default {
  name: "ChartByDateContainer",
  components: { ChartByDate, Loading },
  data: () => ({
    loading: true,
    loaded: false,
    chartdata: null,
    lastUpdated: null
  }),
  async mounted() {
    this.loaded = false;
    this.getData();
  },
  methods: {
    getData: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw/2/public/basic?alt=json"
        )
        .then(response => {
          const responseData = response.data;
          const lastUpdated = new Date(responseData["feed"]["updated"]["$t"]);
          let dateLabels = [];
          let excludedRowIds = [];
          let dailyF = [];
          let dailyM = [];
          for (let i = 0; i < responseData.feed.entry.length; i++) {
            if (
              responseData.feed.entry[i]["title"]["$t"].substring(0, 1) == "A"
            ) {
              if (
                responseData.feed.entry[i]["content"]["$t"].substring(0, 4) ==
                "2020"
              ) {
                dateLabels.push(responseData.feed.entry[i]["content"]["$t"]);
              } else {
                excludedRowIds.push(
                  responseData.feed.entry[i]["title"]["$t"].substring(1)
                );
              }
            }
          }
          for (let i = 0; i < responseData.feed.entry.length; i++) {
            switch (responseData.feed.entry[i]["title"]["$t"].substring(0, 1)) {
              case "B":
                if (
                  !excludedRowIds.includes(
                    responseData.feed.entry[i]["title"]["$t"].substring(1)
                  )
                ) {
                  dailyF.push(responseData.feed.entry[i]["content"]["$t"]);
                }
                break;
              case "C":
                if (
                  !excludedRowIds.includes(
                    responseData.feed.entry[i]["title"]["$t"].substring(1)
                  )
                ) {
                  dailyM.push(responseData.feed.entry[i]["content"]["$t"]);
                }
                break;
              default:
                break;
            }
          }
          this.chartdata = {
            labels: dateLabels,
            datasets: [
              {
                label: "Female",
                backgroundColor: "#42b983",
                data: dailyF
              },
              {
                label: "Male",
                backgroundColor: "#423383",
                data: dailyM
              }
            ]
          };
          this.options = {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
              xAxes: [
                {
                  stacked: true
                }
              ],
              yAxes: [
                {
                  ticks: {
                    beginAtZero: true
                  },
                  stacked: true
                }
              ]
            }
          };
          this.lastUpdated = lastUpdated;
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
  background-color: #fcfcfc;
  margin: 0;
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
