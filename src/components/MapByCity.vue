<template>
  <div class="map-container">
    <h2>Cumulative cases by city</h2>
    <p class="muted">
      Hover or tap on a circle marker in the map to view details.
    </p>
    <l-map :zoom="zoom" :center="center" :options="options" class="map">
      <l-tile-layer :url="url" :attribution="attribution" />
      <l-circle-marker
        v-for="circle in circles"
        :key="circle.id"
        :lat-lng="circle.center"
        :radius="circle.radius"
        :color="circle.color"
      >
        <l-tooltip class="tooltip">
          {{ circle.name }}
        </l-tooltip>
      </l-circle-marker>
    </l-map>
  </div>
</template>

<script>
import L from "leaflet";
import { LMap, LTileLayer, LCircleMarker, LTooltip } from "vue2-leaflet";
import axios from "axios";
import { isMobile } from "mobile-device-detect";

export default {
  name: "MapByCity",
  components: {
    LCircleMarker,
    LMap,
    LTileLayer,
    LTooltip
  },
  data() {
    return {
      zoom: isMobile ? 9 : 11,
      center: [34.75, 135.05],
      url:
        "https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.png",
      attribution:
        'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      circles: [],
      options: {
        scrollWheelZoom: false,
        dragging: !L.Browser.mobile,
        tap: !L.Browser.mobile
      },
      window: {
        height: 0,
        width: 0
      }
    };
  },
  computed: {},
  created() {
    window.addEventListener("resize", this.handleResize);
    this.handleResize();
  },
  mounted() {
    this.getData();
  },
  methods: {
    getData: function() {
      axios
        .get(
          "https://spreadsheets.google.com/feeds/cells/" +
            "1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw" +
            "/3/public/basic?alt=json"
        )
        .then(response => {
          const responseData = response.data;
          const entries = responseData.feed.entry;
          const dimension = this.getDimension(entries);
          let cities = [];

          while (entries.length)
            cities.push(entries.splice(0, dimension.colCount));

          if (isNaN(cities[0][0]["content"]["$t"])) {
            cities.shift();
          }

          cities.forEach(city => {
            const data = {
              center: [
                Number(city[0]["content"]["$t"]),
                Number(city[1]["content"]["$t"])
              ],
              radius: this.calculateRadius(Number(city[3]["content"]["$t"])),
              color: "#00cdbb",
              name: city[2]["content"]["$t"] + ": " + city[3]["content"]["$t"]
            };

            this.circles.push(data);
          });
        })
        .catch(error => {
          console.log(error);
        });
    },
    getDimension: function(entries) {
      let colCount = 0;
      let rowCount = 0;

      for (let i = 0; i < entries.length; i++) {
        if (
          entries[i]["title"]["$t"].length == 2 &&
          entries[i]["title"]["$t"].substring(1) == "1"
        ) {
          colCount += 1;
        } else {
          break;
        }
      }

      rowCount = entries.length / colCount;

      return { rowCount, colCount };
    },
    calculateRadius(data) {
      if (this.window.width < 800) {
        return (this.window.width * data) / 800;
      } else {
        return (this.window.width * data) / 1200;
      }
    },
    handleResize() {
      this.window.width = window.innerWidth;
      this.window.height = window.innerHeight;
    }
  }
};
</script>

<style scoped>
.map-container {
  margin: 0 auto;
  padding: 40px 0;
}

.map {
  margin: 0;
  width: 100%;
  height: 100vh;
}

.tooltip {
  font-size: 16px;
}
</style>
