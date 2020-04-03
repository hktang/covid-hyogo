<template>
  <div class="container">
    <p class="muted">
      {{ $t("overview.lastUpdated") }} {{ new Date(lastUpdated) }}
    </p>
    <dl>
      <i18n path="overview.confirmedCases" tag="dt">
        <template v-slot:0>
          {{ totalTested.toLocaleString() }}
        </template>
      </i18n>
      <dd>
        <strong>{{ totalConfirmed.toLocaleString() }}</strong
        ><br />
        <span class="muted">
          <i18n path="overview.confirmedInTested" tag="span">
            <template v-slot:0>
              {{ Math.round(totalTested / totalConfirmed).toLocaleString() }}
            </template>
          </i18n>
          <br />
          <i18n path="overview.oneInPopulation" tag="span">
            <template v-slot:0>
              {{ Math.round(population / totalConfirmed).toLocaleString() }}
            </template>
          </i18n>
        </span>
      </dd>
      <dt>{{ $t("overview.totalDeaths") }}</dt>
      <dd>
        <strong>{{ totalDeaths.toLocaleString() }}</strong
        ><br />
        <span class="muted">
          <i18n path="overview.totalDeathsInConfirmed" tag="span">
            <template v-slot:0>
              {{ Math.round(totalConfirmed / totalDeaths).toLocaleString() }}
            </template> </i18n
          ><br />
          <i18n path="overview.totalDeathsInTested" tag="span">
            <template v-slot:0>
              {{ Math.round(totalTested / totalDeaths).toLocaleString() }}
            </template> </i18n
          ><br />
          <i18n path="overview.oneDeathInPopulation" tag="span">
            <template v-slot:0>
              {{ Math.round(population / totalDeaths).toLocaleString() }}
            </template>
          </i18n></span
        >
      </dd>
    </dl>
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
    dailyF: [],
    dailyM: [],
    dateLabels: [],
    lastUpdated: null,
    totalConfirmed: 0,
    totalTested: 0,
    totalDeaths: 0,
    population: 5460482 // As of 2020/1/1
  }),
  watch: {
    "$i18n.locale": function() {
      this.setChartData();
    }
  },
  async mounted() {
    this.getDailyTests();
    this.getDeathCount();
    this.getDailyData();
    this.loading = false;
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
          let excludedRowIds = [];

          for (let i = 0; i < responseData.feed.entry.length; i++) {
            if (
              responseData.feed.entry[i]["title"]["$t"].substring(0, 1) == "A"
            ) {
              if (
                responseData.feed.entry[i]["content"]["$t"].substring(0, 4) ==
                "2020"
              ) {
                this.dateLabels.push(
                  responseData.feed.entry[i]["content"]["$t"]
                );
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
                  this.dailyF.push(responseData.feed.entry[i]["content"]["$t"]);
                }
                break;
              case "C":
                if (
                  !excludedRowIds.includes(
                    responseData.feed.entry[i]["title"]["$t"].substring(1)
                  )
                ) {
                  this.dailyM.push(responseData.feed.entry[i]["content"]["$t"]);
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
          this.totalConfirmed =
            this.dailyF.reduce((a, b) => Number(a) + Number(b), 0) +
            this.dailyM.reduce((a, b) => Number(a) + Number(b), 0);
          this.loaded = true;
        })
        .catch(error => {
          console.log(error);
        });
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

          this.totalTested = Number(tests[0]["content"]["$t"]);
        })
        .catch(error => {
          console.log(error);
        });
    },
    getDeathCount: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/" +
            "1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw" +
            "/4/public/basic?alt=json"
        )
        .then(response => {
          const entries = response.data.feed.entry;
          let deathCount = 0;

          for (let i = 0; i < entries.length; i++) {
            if (entries[i]["title"]["$t"].substring(0, 1) == "C") {
              if (!isNaN(entries[i]["content"]["$t"])) {
                deathCount += Number(entries[i]["content"]["$t"]);
              }
            }
          }

          this.totalDeaths = deathCount;
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
