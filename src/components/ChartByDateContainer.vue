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
    sevenDayMovingAverage: [],
    dateLabels: [],
    yTicksMax: null
  }),
  watch: {
    "$i18n.locale": function() {
      this.setChartData();
    }
  },
  async mounted() {
    this.setupData();
    this.loading = false;
  },
  methods: {
    setupData: function() {
      this.dailyF = DataByDate.female;
      this.dailyM = DataByDate.male;
      this.sevenDayMovingAverage = DataByDate.sevenDayMovingAverage;
      this.dateLabels = DataByDate.dateLabels;
      this.yTicksMax = Math.ceil(Math.max(...DataByDate.total) / 5) * 5;
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

              const theTotal =
                data.datasets[1].data[tooltipItem.index] +
                data.datasets[2].data[tooltipItem.index];

              const totalLabel = data.datasets[0].totalLabel;

              return `${theLabel}: ${theNumber} (${totalLabel}: ${theTotal})`;
            }
          }
        },
        scales: {
          xAxes: [
            {
              ticks: {
                reverse: true
              },
              gridLines: {
                display: false
              },
              stacked: true
            }
          ],
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
                max: this.yTicksMax
              },
              stacked: true
            },
            {
              id: "no-stack",
              stacked: false,
              display: false,
              type: "linear",
              ticks: {
                beginAtZero: true,
                min: 0,
                max: this.yTicksMax
              }
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
            label: this.$t("daily.sevenDayMovingAverage"),
            totalLabel: this.$t("daily.dailyTotal"),
            data: this.sevenDayMovingAverage,
            yAxisID: "no-stack",
            type: "line",
            tension: 0.2,
            fill: "rgba(25.9%,20%,51.4%,0)",
            pointBackgroundColor: "#f0f0f0",
            borderColor: "rgba(88.2%,34.1%,42.7%, 60%)",
            borderWidth: 1,
            pointRadius: 1
          },
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
    width: 80vw;
    height: 50vh;
  }
}
</style>
