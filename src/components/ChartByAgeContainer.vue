<template>
  <div class="container">
    <h2>Distribution by age group</h2>
    <loading :active.sync="loading"></loading>
    <chart-by-age
      v-if="loaded"
      class="chart"
      :chartdata="chartdata"
      :options="options"
    />
  </div>
</template>

<script>
import axios from "axios";
import ChartByAge from "./BarChart.vue";
import Loading from "vue-loading-overlay";

export default {
  name: "ChartByDateContainer",
  components: { ChartByAge, Loading },
  data: () => ({
    loading: true,
    loaded: false,
    chartdata: null
  }),
  async mounted() {
    this.loaded = false;
    this.getData();
  },
  methods: {
    getData: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw/4/public/basic?alt=json"
        )
        .then(response => {
          const responseData = response.data;
          let ageLabels = [];
          let excludedRowIds = [];
          let count = [];

          for (let i = 0; i < responseData.feed.entry.length; i++) {
            if (
              responseData.feed.entry[i]["title"]["$t"].substring(0, 1) == "A"
            ) {
              if (
                responseData.feed.entry[i]["content"]["$t"].substring(0, 1) !=
                "A"
              ) {
                ageLabels.push(
                  "Age " + responseData.feed.entry[i]["content"]["$t"]
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
                  count.push(responseData.feed.entry[i]["content"]["$t"]);
                }
                break;
              default:
                break;
            }
          }
          this.chartdata = {
            labels: ageLabels,
            datasets: [
              {
                label: "Number of confirmed cases",
                backgroundColor: "#00cdbb",
                data: count
              }
            ]
          };
          this.options = {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
              xAxes: [{}],
              yAxes: [
                {
                  ticks: {
                    beginAtZero: true
                  }
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
