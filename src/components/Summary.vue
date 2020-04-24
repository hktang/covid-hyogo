<template>
  <div class="container">
    <p class="muted">
      {{ $t("overview.lastUpdated") }}
      {{ new Date(lastUpdated) | moment("YYYY-M-D H:mm:ss") }} (JST)
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
          <i18n path="overview.oneDeathInPopulation" tag="span">
            <template v-slot:0>
              {{ Math.round(population / totalDeaths).toLocaleString() }}
            </template>
          </i18n></span
        >
      </dd>
    </dl>
  </div>
</template>

<script>
import DataSummary from "../data/summary.json";

export default {
  name: "Summary",
  components: {},
  data: () => ({
    loaded: false,
    chartdata: null,
    lastUpdated: null,
    totalConfirmed: 0,
    totalTested: 0,
    totalDeaths: 0,
    population: 0
  }),
  watch: {},
  async mounted() {
    this.getSummary();
  },
  methods: {
    getSummary: function() {
      this.lastUpdated = DataSummary.feed.updated.$t;
      this.totalTested = this.getCell(DataSummary, "B1");
      this.totalConfirmed = this.getCell(DataSummary, "B2");
      this.totalDeaths = this.getCell(DataSummary, "B3");
      this.population = this.getCell(DataSummary, "B4");

      this.loaded = true;
    },
    getCell: function(responseData, cell) {
      let data = responseData.feed.entry.filter(entry => {
        return entry["title"]["$t"] === cell;
      });

      return Number(data[0]["content"]["$t"]);
    }
  }
};
</script>

<style scoped>
.container {
  margin: 20px auto;
  padding: 10px 0;
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
  .chart {
    width: 50vw;
    height: 50vh;
  }
}
</style>
