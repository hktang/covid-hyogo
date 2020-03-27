<template>
  <div class="container">
    <h2>Clusters</h2>
    <chart-by-cluster
      v-if="loaded"
      class="chart"
      :chartdata="chartdata"
      :options="options"
    />
    <ul class="legend muted">
      <li v-for="legend in legends" :key="legend.id">
        <strong>{{ legend[0] }}</strong
        >: {{ legend[1] }}
      </li>
    </ul>
  </div>
</template>

<script>
import axios from "axios";
import ChartByCluster from "./ScatterPlot.vue";
import { isMobile } from "mobile-device-detect";

export default {
  name: "ChartByDateContainer",
  components: { ChartByCluster },
  data: () => ({
    loaded: false,
    chartdata: null,
    xLabels: [],
    yLabels: [],
    legends: []
  }),
  async mounted() {
    this.getData();
    this.getLegends();
  },
  methods: {
    getData: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/" +
            "1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw" +
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

          const caseNumberColumn = responseData.feed.entry.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) === "B";
          });

          const cases = responseData.feed.entry.filter(entry => {
            return entry["content"]["$t"].trim() === "〇";
          });

          this.header = headerRow.map(item => item["content"]["$t"]);
          this.yLabels = isMobile
            ? headerRow.map(item => item["content"]["$t"].substring(0, 1))
            : headerRow.map(item => item["content"]["$t"]);
          this.yLabels.splice(0, 2);
          this.xLabels = caseNumberColumn.map(item => item["content"]["$t"]);
          this.xLabels.splice(0, 1);

          const caseData = [];
          let pointRadiusList = [];

          for (let i = 0; i < cases.length; i++) {
            const label = cases[i]["title"]["$t"];
            const rowNum = label.substring(1);
            const colAlpha = label.substring(0, 1);

            const theCaseNumberCell = responseData.feed.entry.filter(entry => {
              return entry["title"]["$t"] === "B" + rowNum;
            });

            const theCluster = responseData.feed.entry.filter(entry => {
              return entry["title"]["$t"] === colAlpha + "1";
            });

            const xValue = this.xLabels.indexOf(
              theCaseNumberCell[0]["content"]["$t"]
            );
            const yValue = isMobile
              ? this.yLabels.indexOf(
                  theCluster[0]["content"]["$t"].substring(0, 1)
                )
              : this.yLabels.indexOf(theCluster[0]["content"]["$t"]);

            const theCase = {
              x: xValue,
              y: yValue,
              toolTip: theCaseNumberCell[0]["content"]["$t"]
            };

            if (isNaN(pointRadiusList[i])) {
              pointRadiusList[i] = 1;
            }

            if (this.containsCase(theCase, caseData)) {
              pointRadiusList[caseData.length - 1] += 1;
            } else {
              caseData.push(theCase);
            }
          }
          this.chartdata = {
            datasets: [
              {
                data: caseData,
                fill: false,
                showLine: false,
                pointRadius: pointRadiusList.map(x => x * 4),
                borderWidth: 1,
                borderColor: "#42b983",
                backgroundColor: "rgba(255, 255, 255, 0.2)"
              }
            ]
          };
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
                  console.log(tooltipItem, data);
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
                    display: true,
                    labelString: "Case No."
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
                    display: true,
                    labelString: "Cluster"
                  },
                  ticks: {
                    reverse: true,
                    min: 0,
                    max: this.yLabels.length - 1,
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
    getLegends: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/" +
            "1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw" +
            "/7/public/basic?alt=json"
        )
        .then(response => {
          const responseData = response.data;

          const jaStrings = responseData.feed.entry.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) === "A";
          });

          const enStrings = responseData.feed.entry.filter(entry => {
            return entry["title"]["$t"].substring(0, 1) === "B";
          });

          for (let i = 0; i < jaStrings.length; i++) {
            this.legends.push([
              jaStrings[i]["content"]["$t"],
              enStrings[i]["content"]["$t"]
            ]);
          }
        })
        .catch(error => {
          console.log(error);
        });
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
