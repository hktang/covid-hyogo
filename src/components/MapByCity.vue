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
        :fill-color="circle.fillColor"
        :fill-opacity="circle.fillOpacity"
        :color="circle.color"
        :weight="circle.weight"
        :opacity="circle.opacity"
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
        "https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png",
      attribution:
        '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
      circles: [],
      max: 0,
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
    this.getMaxCases();
    this.getData();
  },
  methods: {
    getMaxCases: function() {
      let cities = DataByCity.cities;

      cities.forEach(city => {
        if (this.max < city.cases) {
          this.max = city.cases;
        }
      });
    },
    getData: function() {
      let cities = DataByCity.cities;

      cities.forEach(city => {
        const data = {
          center: [city.lat, city.lng],
          radius: this.calculateRadius(city.cases),
          fillColor: "#00cdbb",
          color: "#00cdbb",
          weight: 5,
          opacity: 0.6,
          fillOpacity: 0.1,
          name: city.name + ": " + city.cases
        };

        this.circles.push(data);
      });
    },
    calculateRadius(data) {
      const scale = this.window.width / 8 / this.max;
      return data * scale;
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
