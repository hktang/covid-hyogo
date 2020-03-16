<template>
  <div class="container">
    <h2>Clusters</h2>
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
    xLabels: [],
    yLabels: []
  }),
  async mounted() {
    this.getData();
  },
  methods: {
    getData: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/" +
            process.env.VUE_APP_GOOGLE_SPREADSHEET_ID +
            "/6/public/basic?alt=json"
        )
        .then(response => {
          const responseData = response.data;

          const headerRow = responseData.feed.entry.filter(entry => {
            return (
              entry["title"]["$t"].substring(1, 2) === "1" &&
              entry["title"]["$t"].length == 2
            );
          });

          const dateColumn = responseData.feed.entry.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) === "B";
          });

          const cases = responseData.feed.entry.filter(entry => {
            return entry["content"]["$t"].trim() === "〇";
          });

          this.header = headerRow.map(item => item["content"]["$t"]);
          this.xLabels = headerRow.map(item => item["content"]["$t"]);
          this.xLabels.splice(0, 2);
          this.yLabels = dateColumn.map(item => item["content"]["$t"]);
          this.yLabels.splice(0, 1);

          const caseData = [];

          for (let i = 0; i < cases.length; i++) {
            const label = cases[i]["title"]["$t"];
            const rowNum = label.substring(1);
            const colAlpha = label.substring(0, 1);

            const theDate = responseData.feed.entry.filter(entry => {
              return entry["title"]["$t"] === "B" + rowNum;
            });

            const theLabel = responseData.feed.entry.filter(entry => {
              return entry["title"]["$t"] === colAlpha + "1";
            });

            caseData.push(
              this.mapDataPoint(
                theLabel[0]["content"]["$t"],
                theDate[0]["content"]["$t"]
              )
            );
          }

          this.chartdata = {
            datasets: [
              {
                data: caseData,
                fill: false,
                showLine: false,
                opacity: 0.5,
                pointRadius: 4,
                borderWidth: 2,
                borderColor: "#809399",
                backgroundColor: "rgba(255, 255, 255, 0)"
              }
            ]
          };
          this.options = {
            responsive: true,
            maintainAspectRatio: true,
            aspectRatio: 0.2,
            title: {
              display: false
            },
            legend: {
              display: false
            },
            tooltips: {
              enabled: false
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
                    max: this.xLabels.length - 1,
                    callback: value => {
                      return this.xLabels[value];
                    }
                  }
                }
              ],
              yAxes: [
                {
                  type: "linear",
                  scaleLabel: {
                    display: false
                  },
                  gridLines: {
                    display: false
                  },
                  ticks: {
                    reverse: false,
                    min: 0,
                    max: this.yLabels.length + 1,
                    callback: i => {
                      return this.yLabels[i];
                    }
                  }
                }
              ]
            }
          };
          this.loaded = true;
        })
        .catch(error => {
          console.log(error);
        });
    },
    // Courtesy of https://stackoverflow.com/questions/43090102/chartjs-mapping-non-numeric-y-and-x
    mapDataPoint: function(xValue, yValue) {
      return {
        x: this.xLabels.indexOf(xValue),
        y: this.yLabels.indexOf(yValue)
      };
    }
  }
};
</script>

<style scoped>
.container {
  margin: 0 auto;
  padding-bottom: 40px;
}

.chart {
}

@media only screen and (max-width: 800px) {
  .container {
    width: 95vw;
  }
}

@media only screen and (min-width: 800px) {
  .container {
    width: 50vw;
  }
}
</style>
