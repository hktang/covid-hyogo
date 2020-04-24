<template>
  <div class="container">
    <h2>{{ $t("age.title") }}</h2>
    <loading :active.sync="loading"></loading>
    <chart-by-age
      v-if="loaded"
      class="chart"
      :chart-data="chartdata"
      :options="options"
    />
  </div>
</template>

<script>
import ChartByAge from "./BarChart.vue";
import Loading from "vue-loading-overlay";
import DataByAge from "../data/byAge.json";

export default {
  name: "ChartByDateContainer",
  components: { ChartByAge, Loading },
  data: () => ({
    chartdata: null,
    counts: [],
    deathCounts: [],
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
    getLabels: function() {
      const labels = this.$t("age.labels");
      return Object.values(labels);
    },
    setChartData: function() {
      this.chartdata = {
        labels: this.getLabels(),
        datasets: [
          {
            label: this.$t("status.labels.confirmed"),
            backgroundColor: "#42b983",
            data: this.counts.map(x => (x > 0 ? x : 0))
          },
          {
            label: this.$t("age.deceased"),
            backgroundColor: "#5c5c5c",
            data: this.deathCounts
          }
        ]
      };
    },
    getData: function() {
      let excludedRowIds = ["1"];
      const entries = DataByAge.feed.entry;

      for (let i = 0; i < entries.length; i++) {
        switch (entries[i]["title"]["$t"].substring(0, 1)) {
          case "B":
            if (
              !excludedRowIds.includes(entries[i]["title"]["$t"].substring(1))
            ) {
              this.counts.push(Number(entries[i]["content"]["$t"]));
              this.deathCounts.push(0);
            }
            break;
          case "C":
            if (
              !excludedRowIds.includes(entries[i]["title"]["$t"].substring(1))
            ) {
              this.deathCounts[this.deathCounts.length - 1] += Number(
                entries[i]["content"]["$t"]
              );
            }
            break;
          default:
            break;
        }
      }
      this.setChartData();
      this.options = {
        maintainAspectRatio: false,
        responsive: true,
        tooltips: {
          enabled: true,
          callbacks: {
            label: function(tooltipItem, data) {
              const theLabel = data.datasets[tooltipItem.datasetIndex].label;

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
              stacked: false
            }
          ],
          yAxes: [
            {
              ticks: {
                beginAtZero: true
              },
              stacked: false
            }
          ]
        }
      };
      this.loaded = true;
      this.loading = false;
    }
  }
};
</script>

<style scoped>
.container {
  margin: 20px auto;
  padding: 20px 0 50px;
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
