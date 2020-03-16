<template>
  <div class="container">
    <p class="muted">Last updated: {{ new Date(lastUpdated) }}</p>
    <dl>
      <dt>Total confirmed cases out of the {{ totalTested }} tested</dt>
      <dd>
        <strong>{{ totalConfirmed }}</strong
        ><br />
        <span class="muted">
          ...that is 1 in
          {{ Math.round(totalTested / totalConfirmed).toLocaleString() }}
          patients tested so far;<br />
          or 1 in
          {{ Math.round(population / totalConfirmed).toLocaleString() }}
          residents of Hyogo Prefecture.</span
        >
      </dd>
      <dt>Total deaths</dt>
      <dd>
        <strong>{{ totalDeaths }}</strong
        ><br />
        <span class="muted">
          ... that is 1 in
          {{ Math.round(totalConfirmed / totalDeaths).toLocaleString() }}
          confirmed cases; <br />
          or 1 in
          {{ Math.round(totalTested / totalDeaths).toLocaleString() }}
          patients tested so far;<br />
          or 1 in
          {{ Math.round(population / totalDeaths).toLocaleString() }} residents
          of Hyogo Prefecture.</span
        >
      </dd>
    </dl>
    <h3>Daily confirmed cases</h3>
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
import ChartByDate from "./BarChart.vue";
import Loading from "vue-loading-overlay";

export default {
  name: "ChartByDateContainer",
  components: { ChartByDate, Loading },
  data: () => ({
    loading: true,
    loaded: false,
    chartdata: null,
    lastUpdated: null,
    totalConfirmed: null,
    totalTested: null,
    totalDeaths: null,
    population: 5460482 // As of 2020/1/1
  }),
  async mounted() {
    this.getDailyData();
    this.getDailyTests();
  },
  methods: {
    getDailyData: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/" +
            "1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw" +
            "/2/public/basic?alt=json"
        )
        .then(response => {
          const responseData = response.data;
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
              case "D":
                if (responseData.feed.entry[i]["title"]["$t"] == "D1") {
                  this.lastUpdated =
                    responseData.feed.entry[i]["content"]["$t"];
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
          this.totalConfirmed =
            dailyF.reduce((a, b) => Number(a) + Number(b), 0) +
            dailyM.reduce((a, b) => Number(a) + Number(b), 0);
          this.loaded = true;
          this.loading = false;
        })
        .catch(error => {
          console.log(error);
        });
    },
    getDailyTests: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/" +
            "1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw" +
            "/5/public/basic?alt=json"
        )
        .then(response => {
          const responseData = response.data;

          //B2: Tests conducted
          let tests = responseData.feed.entry.filter(entry => {
            return entry["title"]["$t"] === "B2";
          });

          //G2: Deaths
          let deaths = responseData.feed.entry.filter(entry => {
            return entry["title"]["$t"] === "G2";
          });

          this.totalTested = Number(tests[0]["content"]["$t"]);
          this.totalDeaths = Number(deaths[0]["content"]["$t"]);
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
    min-height: 50vh;
  }

  .chart {
    width: 50vw;
    height: 50vh;
  }
}
</style>
