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

            const theCase = {
              x: this.xLabels.indexOf(theCluster[0]["content"]["$t"]),
              y: this.yLabels.indexOf(theCaseNumberCell[0]["content"]["$t"]),
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
                opacity: 0.5,
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
                  ticks: {
                    min: 0,
                    max: this.xLabels.length - 1,
                    callback: value => {
                      return this.xLabels[value];
                    },
                    minRotation: 75,
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
                  gridLines: {
                    display: false
                  },
                  ticks: {
                    reverse: false,
                    min: 0,
                    max: this.yLabels.length,
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
  margin: 0 auto;
  padding-bottom: 40px;
}

.legend {
  font-size: 12px;
  padding-left: 20px;
}

ul.legend li {
  text-align: left;
  list-style-type: square;
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
