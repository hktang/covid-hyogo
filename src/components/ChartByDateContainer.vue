<template>
  <div class="container">
    <h3>{{ $t("daily.title") }}</h3>
    <loading :active.sync="loading"></loading>
    <chart-by-date
      v-if="loaded"
      class="chart"
      :chart-data="chartdata"
      :options="options"
    />
  </div>
</template>

<script>
import ChartByDate from "./BarChart.vue";
import Loading from "vue-loading-overlay";
import DataByDate from "../data/byDate.json";

export default {
  name: "ChartByDateContainer",
  components: { ChartByDate, Loading },
  data: () => ({
    loading: true,
    loaded: false,
    chartdata: null,
    dailyF: [],
    dailyM: [],
    dateLabels: []
  }),
  watch: {
    "$i18n.locale": function() {
      this.setChartData();
    }
  },
  async mounted() {
    this.getDailyData();
    this.loading = false;
  },
  methods: {
    getDailyData: function() {
      let excludedRowIds = [];

      for (let i = 0; i < DataByDate.feed.entry.length; i++) {
        if (DataByDate.feed.entry[i]["title"]["$t"].substring(0, 1) == "A") {
          if (
            DataByDate.feed.entry[i]["content"]["$t"].substring(0, 4) == "2020"
          ) {
            this.dateLabels.push(DataByDate.feed.entry[i]["content"]["$t"]);
          } else {
            excludedRowIds.push(
              DataByDate.feed.entry[i]["title"]["$t"].substring(1)
            );
          }
        }
      }
      for (let i = 0; i < DataByDate.feed.entry.length; i++) {
        switch (DataByDate.feed.entry[i]["title"]["$t"].substring(0, 1)) {
          case "B":
            if (
              !excludedRowIds.includes(
                DataByDate.feed.entry[i]["title"]["$t"].substring(1)
              )
            ) {
              this.dailyF.push(DataByDate.feed.entry[i]["content"]["$t"]);
            }
            break;
          case "C":
            if (
              !excludedRowIds.includes(
                DataByDate.feed.entry[i]["title"]["$t"].substring(1)
              )
            ) {
              this.dailyM.push(DataByDate.feed.entry[i]["content"]["$t"]);
            }
            break;
          case "D":
            if (DataByDate.feed.entry[i]["title"]["$t"] == "D1") {
              this.lastUpdated = DataByDate.feed.entry[i]["content"]["$t"];
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
      this.loaded = true;
    },
    setChartData: function() {
      this.chartdata = {
        labels: this.dateLabels,
        datasets: [
          {
            label: this.$t("daily.female"),
            backgroundColor: "#42b983",
            data: this.dailyF
          },
          {
            label: this.$t("daily.male"),
            backgroundColor: "#423383",
            data: this.dailyM
          }
        ]
      };
    }
  }
};
</script>

<style scoped>
.container {
  background-color: #fafafa;
  margin: 20px auto;
  padding: 10px 0 50px;
}

.chart {
  padding: 0;
  margin: 0 auto;
}

dt {
  padding-top: 24px;
  color: #42b983;
  font-weight: 900;
}
dd {
  margin: 12px 0 0 0;
  font-size: 26px;
  line-height: 20px;
}
h3 {
  margin-top: 50px;
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
    min-height: 300px;
  }

  .chart {
    width: 50vw;
    height: 50vh;
  }
}
</style>
