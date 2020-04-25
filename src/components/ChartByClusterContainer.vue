<template>
  <div class="container">
    <h2>{{ $t("clusters.title") }}</h2>
    <chart-by-cluster
      v-if="loaded"
      class="chart"
      :chart-data="chartdata"
      :options="options"
    />
    <p class="legend muted">
      <span v-for="(legend, key) in legends" :key="legend">
        <strong>({{ key }})</strong> {{ legend }}
      </span>
    </p>
  </div>
</template>

<script>
import ChartByCluster from "./ScatterPlot.vue";
import { isMobile } from "mobile-device-detect";
import DataByCluster from "../data/byCluster.json";

export default {
  name: "ChartByDateContainer",
  components: { ChartByCluster },
  data: () => ({
    loaded: false,
    caseData: [],
    chartdata: null,
    xLabels: [],
    yLabels: [],
    legends: []
  }),
  watch: {
    "$i18n.locale": function() {
      this.getLegends();
    }
  },
  async mounted() {
    this.getData();
    this.getLegends();
  },
  methods: {
    setChartData: function() {
      this.chartdata = {
        datasets: [
          {
            data: this.caseData,
            fill: false,
            showLine: false,
            pointRadius: 4,
            borderWidth: 1,
            borderColor: "#42b983",
            backgroundColor: "rgba(255, 255, 255, 0.2)"
          }
        ]
      };
    },
    getData: function() {
      const cases = DataByCluster.caseVsCluster;
      const originalCols = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

      this.xLabels = DataByCluster.caseNumber;
      this.yLabels = isMobile
        ? Object.values(DataByCluster.clusters).map(value =>
            value.substring(0, 1)
          )
        : Object.values(DataByCluster.clusters);

      for (let i = 0; i < cases.length; i++) {
        const label = cases[i];
        const caseId = label.substring(1) - 2;

        const theCase = {
          x: caseId,
          y: originalCols.indexOf(label.substring(0, 1)) - 2,
          toolTip: DataByCluster.caseNumber[caseId]
        };

        this.caseData.push(theCase);
      }

      this.setChartData();

      this.options = {
        responsive: true,
        maintainAspectRatio: false,
        title: {
          display: false
        },
        legend: {
          display: false
        },
        tooltips: {
          enabled: true,
          callbacks: {
            label: function(tooltipItem, data) {
              return data.datasets[0].data[tooltipItem.index].toolTip;
            }
          }
        },
        scales: {
          xAxes: [
            {
              type: "linear",
              position: "top",
              gridLines: {
                display: false
              },
              scaleLabel: {
                display: false
              },
              ticks: {
                min: 0,
                reverse: true,
                max: this.xLabels.length,
                callback: value => {
                  return this.xLabels[value];
                },
                autoSkip: false
              }
            }
          ],
          yAxes: [
            {
              type: "linear",
              scaleLabel: {
                display: false
              },
              ticks: {
                reverse: true,
                min: 0,
                max: this.yLabels.length - 1,
                maxTicksLimit: this.yLabels.length,
                callback: i => {
                  return this.yLabels[i];
                }
              }
            }
          ]
        }
      };
      this.loaded = true;
    },
    getLegends: function() {
      this.legends = this.$t("clusters.labels");
    },
    containsCase: function(object, list) {
      var i;
      for (i = 0; i < list.length; i++) {
        if (list[i].x === object.x) {
          if (list[i].y === object.y) {
            return true;
          }
        }
      }
      return false;
    }
  }
};
</script>

<style scoped>
.container {
  margin: 20px auto;
  padding: 20px 0 50px;
  padding-bottom: 40px;
}

.legend {
  font-size: 12px;
  margin: 20px 0 0 -10px;
}

ul.legend li {
  text-align: left;
  list-style-type: square;
}

@media only screen and (max-width: 800px) {
  .container {
    width: 98vw;
  }
}

@media only screen and (min-width: 800px) {
  .container {
    width: 66vw;
  }
}
</style>
