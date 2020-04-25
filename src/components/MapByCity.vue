<template>
  <div class="map-container">
    <h2>{{ $t("city.title") }}</h2>
    <p class="muted">{{ $t("city.tip") }}</p>
    <l-map
      :zoom="zoom"
      :center="center"
      :options="options"
      class="map"
      @update:zoom="zoomUpdated"
    >
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
import { isMobile } from "mobile-device-detect";
import DataByCity from "../data/byCity.json";

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
      let cities = DataByCity.cities;

      cities.forEach(city => {
        const data = {
          center: [city.lat, city.lng],
          radius: this.calculateRadius(city.cases),
          color: "#00cdbb",
          name: city.name + ": " + city.cases
        };

        this.circles.push(data);
      });
    },
    calculateRadius(data) {
      if (this.window.width < 800) {
        return (this.window.width * data) / 1400;
      } else {
        return (this.window.width * data) / 1600;
      }
    },
    handleResize() {
      this.window.width = window.innerWidth;
      this.window.height = window.innerHeight;
    },
    zoomUpdated(newZoom) {
      if (Number(this.zoom - newZoom) > 0) {
        this.circles.forEach(circle => (circle.radius /= 2));
      } else if (Number(this.zoom - newZoom) < 0) {
        this.circles.forEach(circle => (circle.radius *= 2));
      }
      this.zoom = newZoom;
    }
  }
};
</script>

<style scoped>
.map-container {
  margin: 0 auto;
  padding: 20px 0 40px 0;
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
