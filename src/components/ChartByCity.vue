<template>
  <div class="container">
    <h2>Accumulated cases by city</h2>
    <l-map
      :zoom="zoom"
      :center="center"
      :options="{scrollWheelZoom:false}"
      class="map"
    >
      <l-tile-layer
        :url="url"
        :attribution="attribution"
      />
      <l-circle-marker
        v-for="circle in circles"
        v-bind:key="circle.id"
        :lat-lng="circle.center"
        :radius="circle.radius"
        :color="circle.color"
      >
        <l-tooltip>
         {{circle.name}}
        </l-tooltip>
      </l-circle-marker>
    </l-map>
  </div>
</template>

<script>
import {LMap, LTileLayer, LCircleMarker, LTooltip} from 'vue2-leaflet'
import axios from 'axios'

export default {
  name: "ChartByCity",
  components: {
    LCircleMarker,
    LMap,
    LTileLayer,
    LTooltip
  },
  data() {
    return {
      zoom: 10,
      center: [34.833439, 134.993893],
      url: 'https://tiles.stadiamaps.com/tiles/alidade_smooth/{z}/{x}/{y}{r}.png',
      attribution: '&copy; <a href="https://stadiamaps.com/">Stadia Maps</a>, &copy; <a href="https://openmaptiles.org/">OpenMapTiles</a> &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors',
      circles: [],
    }
  },
  methods: {
    getData: function() {
      axios.get('https://spreadsheets.google.com/feeds/cells/1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw/3/public/basic?alt=json')
        .then(response => {

          const responseData = response.data
          const entries = responseData.feed.entry
          const dimension = this.getDimension(entries)
          let cities = []

          while(entries.length) cities.push(entries.splice(0,dimension.colCount));

          if(isNaN(cities[0][0]['content']['$t'] )) {
            cities.shift()
          }

          cities.forEach((city) => {

            const data = {
              center: [Number(city[0]['content']['$t']), 
                       Number(city[1]['content']['$t'])],
              radius: Number(city[3]['content']['$t']) * 1.5,
              color: '#64b5c2',
              name: city[2]['content']['$t'] + ': ' + city[3]['content']['$t']
            }

            this.circles.push(data)
          })
          console.log(this.circles)
        }).catch(error => {
          console.log(error)
      });
    },
    getDimension: function(entries) {
      //let cities = []
      let colCount = 0
      let rowCount = 0

      for (let i=0; i < entries.length; i++){
        if(entries[i]['title']['$t'].length == 2 
        && entries[i]['title']['$t'].substring(1) == "1"){
          colCount += 1
        }else{
          break
        }
      }

      rowCount = entries.length / colCount;

      return {rowCount, colCount}
    }
  },
  async mounted() {
    this.getData()
  },
  computed: {}
};
</script>

<style scoped>

.container{
  margin: 0 auto;
  padding: 60px 0;
}

.map {
  margin: 0;
}

@media only screen and (max-width: 800px) {

  .container {
    width: 100%;
    height: 30vh;
  }
}

@media only screen and (min-width: 800px) {

  .container {
    width: 100%;
    height: 100vh;
  }
}
</style>
