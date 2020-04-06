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
    capacity: [],
    dateLabels: [],
    nonSevere: [],
    severe: [],
    deaths: [],
    discharged: [],
    totalPositive: [],
    loaded: false,
    loading: true
  }),
  computed: {
    maxY: function() {
      const totalPositive = this.totalPositive.map(c => Number(c));
      const maxPositive = Math.ceil(Math.max(...totalPositive) / 100) * 100;
      const totalCapacity = this.capacity.map(c => Number(c));
      const maxCapacity = Math.ceil(Math.max(...totalCapacity) / 100) * 100;

      return maxPositive > maxCapacity ? maxPositive : maxCapacity;
    },
    maxOthers: function() {
      return Math.floor((this.deaths[0] + this.discharged[0]) / 100) * 100;
    }
  },
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
            backgroundColor: "#276a4c",
            data: this.severe
          },
          {
            label: this.$t("age.deceased"),
            backgroundColor: "#7c7f7e",
            data: this.deaths
          },
          {
            label: this.$t("status.labels.discharged"),
            backgroundColor: "#addcf3",
            data: this.discharged
          },
          {
            label: this.$t("status.labels.confirmed"),
            backgroundColor: "#f0f0f0",
            borderColor: "#42b983",
            borderWidth: 1,
            pointRadius: 2,
            data: this.totalPositive,
            type: "line"
          },
          {
            label: this.$t("capacity.labels.beds"),
            fill: "rgba(25.9%,20%,51.4%,0)",
            pointBackgroundColor: "#423383",
            borderColor: "#423383",
            borderWidth: 2,
            pointRadius: 2,
            type: "line",
            data: this.capacity,
            yAxisID: "no-stack",
            spanGaps: true,
            //tension: 0,
            borderDash: [2, 6]
          }
        ]
      };
    },
    getData: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/" +
            "1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw" +
            "/7/public/basic?alt=json"
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
          this.deaths = deathCases.map(c => c["content"]["$t"] * -1);
          this.deaths.shift();

          const dischargedCases = entries.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) == "H";
          });
          this.discharged = dischargedCases.map(c => c["content"]["$t"] * -1);
          this.discharged.shift();

          const capacityCount = entries.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) == "I";
          });

          console.log(capacityCount);

          this.capacity = capacityCount.map(c =>
            isNaN(c["content"]["$t"]) ? null : c["content"]["$t"]
          );
          this.capacity.shift();

          console.log(this.capacity);

          this.setChartData();

          this.options = {
            maintainAspectRatio: false,
            responsive: true,
            elements: {
              point: {
                radius: 0
              }
            },
            tooltips: {
              enabled: true,
              callbacks: {
                label: function(tooltipItem, data) {
                  const theLabel =
                    data.datasets[tooltipItem.datasetIndex].label;

                  const theNumber = Math.abs(
                    Number(
                      data.datasets[tooltipItem.datasetIndex].data[
                        tooltipItem.index
                      ]
                    )
                  );

                  return theLabel + ": " + theNumber;
                }
              }
            },
            scales: {
              xAxes: [
                {
                  stacked: true,
                  ticks: {
                    reverse: true
                  },
                  gridLines: {
                    display: false
                  }
                }
              ],
              yAxes: [
                {
                  stacked: true,
                  ticks: {
                    beginAtZero: true,
                    min: this.maxOthers,
                    max: this.maxY
                  }
                },
                {
                  id: "no-stack",
                  stacked: false,
                  display: false,
                  ticks: {
                    beginAtZero: true,
                    min: this.maxOthers,
                    max: this.maxY
                  },
                  type: "linear"
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
