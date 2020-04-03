<template>
  <div class="container">
    <h2>{{ $t("status.title") }}</h2>
    <loading :active.sync="loading"></loading>
    <chart-by-status
      v-if="loaded"
      class="chart"
      :chart-data="chartdata"
      :options="options"
    />
  </div>
</template>

<script>
import axios from "axios";
import ChartByStatus from "./BarChart.vue";
import Loading from "vue-loading-overlay";

export default {
  name: "ChartByDateContainer",
  components: { ChartByStatus, Loading },
  data: () => ({
    chartdata: null,
    dateLabels: [],
    nonSevere: [],
    severe: [],
    deaths: [],
    discharged: [],
    totalPositive: [],
    loaded: false,
    loading: true
  }),
  watch: {
    "$i18n.locale": function() {
      this.setChartData();
    }
  },
  async mounted() {
    this.getData();
  },
  methods: {
    setChartData: function() {
      this.chartdata = {
        labels: this.dateLabels,
        datasets: [
          {
            label: this.$t("status.labels.nonSevere"),
            backgroundColor: "#42b983",
            data: this.nonSevere
          },
          {
            label: this.$t("status.labels.severe"),
            backgroundColor: "#194531",
            data: this.severe
          },
          {
            label: this.$t("status.labels.deaths"),
            backgroundColor: "#7c7f7e",
            data: this.deaths
          },
          {
            label: this.$t("status.labels.discharged"),
            backgroundColor: "#b98342",
            data: this.discharged
          },
          {
            label: this.$t("status.labels.confirmed"),
            backgroundColor: "#c2ead7",
            borderColor: "#42b983",
            borderWidth: 1,
            data: this.totalPositive,
            type: "line"
          }
        ]
      };
    },
    getData: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/" +
            "1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw" +
            "/5/public/basic?alt=json"
        )
        .then(response => {
          const responseData = response.data;

          const entries = responseData.feed.entry;

          for (let i = 0; i < entries.length; i++) {
            if (entries[i]["title"]["$t"].substring(0, 1) == "A") {
              if (!isNaN(entries[i]["content"]["$t"].substring(0, 4))) {
                this.dateLabels.push(entries[i]["content"]["$t"]);
              }
            }
          }

          const totalPositiveCases = entries.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) == "C";
          });
          this.totalPositive = totalPositiveCases.map(c => c["content"]["$t"]);
          this.totalPositive.shift();

          const nonSevereCases = entries.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) == "E";
          });
          this.nonSevere = nonSevereCases.map(c => c["content"]["$t"]);
          this.nonSevere.shift();

          const severeCases = entries.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) == "F";
          });
          this.severe = severeCases.map(c => c["content"]["$t"]);
          this.severe.shift();

          const deathCases = entries.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) == "G";
          });
          this.deaths = deathCases.map(c => c["content"]["$t"]);
          this.deaths.shift();

          const dischargedCases = entries.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) == "H";
          });
          this.discharged = dischargedCases.map(c => c["content"]["$t"]);
          this.discharged.shift();

          this.setChartData();

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
