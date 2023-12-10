<template>
  <div id="map">
  </div>
  <q-card flat class="q-pa-sm"
    style="width:100%;position:absolute;top:0px;left:50%;transform:translateX(-50%);z-index:1000;background: rgba(255, 255, 255, 0);border-radius: 25px;">
    <div class="row items-center">
      <div class="col-10 q-pl-xs">
        <q-img src="logo_letters.svg" style="height:30px;width:100px"></q-img>
      </div>
      <div class="col-2">
        <div class="text-right"><q-btn rounded color="white" text-color="black" icon="menu" /></div>
      </div>
    </div>
  </q-card>

  <q-card v-if="home" class="q-pa-md" flat
    style="width:100%;height:80%;position:absolute;top:0px;left:50%;transform:translateX(-50%);z-index:999;background: rgba(255, 255, 255, 0.5)">
    <div class="row text-center fit items-center">
      <div class="col-12">
        <q-img src="logo.svg" style="height: 260px; max-width: 260px"></q-img>
      </div>
    </div>
  </q-card>

  <q-dialog persistent seamless position="bottom" v-model="getLocationDialog">
    <q-card class="bg-white q-pa-none" style="width:100%;border-top-left-radius: 25px;border-top-right-radius: 25px;">
      <q-card-section>
        <div class="row">
          <div class="col-12 text-center text-h5">
            where are you?
          </div>
        </div>
        <div class="row">
          <div class="col-12 q-pa-sm text-center">
            <q-btn icon="my_location" size="md" @click="geoLocateUser()">use my location</q-btn>
          </div>
          <div class="col-12 q-pa-sm text-center">
            <q-btn icon="location_on" size="md" @click="selectLocationOnMap">select on map</q-btn>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-dialog persistent seamless position="bottom" v-model="locatingDialog">
    <q-card class="bg-white q-pa-none" style="width:100%;border-top-left-radius: 25px;border-top-right-radius: 25px;">
      <q-card-section>
        <div class="row">
          <div class="col-12 text-center text-h5">
            locating...
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-dialog persistent seamless position="bottom" v-model="selectLocationOnMapDialog">
    <q-card class="bg-white q-pa-none" style="width:100%;border-top-left-radius: 25px;border-top-right-radius: 25px;">
      <q-card-section>
        <div class="row justify-center">
          <div class="col-12 q-pa-md">
            <div class="text-center">drag the map to move the pin as closely to your location and press the confirm button
            </div>
          </div>
          <div class="col-12 q-pa-md">
            <div class="text-center text-weight-bold">{{ userAddress }}</div>
          </div>
          <div class="col-12 text-center">
            <q-btn @click="confirmLocation" no-caps class="bg-green-8 text-white text-h6">confirm location</q-btn>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-dialog persistent seamless position="bottom" v-model="getMaximumDistanceDialog">
    <q-card class="bg-white q-pa-none" style="width:100%;border-top-left-radius: 25px;border-top-right-radius: 25px;">
      <q-card-section>
        <div class="row">
          <div class="col-12 text-center text-body1">
            max driving distance to charging station
          </div>
        </div>
        <div class="row">
          <div class="col-12 q-px-md text-center text-h4">
            {{ maximumChargingPointDistance }} Km
          </div>
          <div class="col-12 q-pt-md q-px-md text-center">
            <q-slider v-model="maximumChargingPointDistance" :min="5" :max="60" :step="5" snap label label-always
              track-size="10px" color="green" />
          </div>
          <div class="col-12 q-px-md text-center text-h4">
            <q-btn size="lg" color="green" @click="getChargingTime">next</q-btn>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-dialog persistent seamless position="bottom" v-model="selectChargingTimeDialog">
    <q-card class="bg-white q-pa-none" style="width:100%;border-top-left-radius: 25px;border-top-right-radius: 25px;">
      <q-card-section>
        <div class="row">
          <div class="col-12 text-center text-body1">
            when would you like to charge your car?
          </div>
        </div>
        <div class="row">
          <div class="col-12 q-px-md text-center text-h4">
            <VueDatePicker v-model="selectedTime" :teleport="true" minutes-increment="15" time-picker></VueDatePicker>
          </div>
          <div class="col-12 q-px-md q-py-lg text-center text-h6">
            <q-btn size="md" color="green" @click="getRecommendation">recommend charging points!</q-btn>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-dialog persistent seamless position="bottom" v-model="loadingDialog">
    <q-card class="bg-white q-pa-none" style="width:100%;border-top-left-radius: 25px;border-top-right-radius: 25px;">
      <q-card-section>
        <div class="row">
          <div class="col-12 text-center text-body1">
            finding the best charging stations nearby...
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-dialog seamless position="bottom" v-model="showRecommendationsDialog">
    <div class="row justify-between q-pa-md">
      <div clas="col-4">

      </div>
      <div clas="col-4">
        <q-btn no-caps class="bg-green text-white q-px-lg" @click="rateDialog = true">finish</q-btn>
      </div>
    </div>
    <q-card class="bg-white q-pa-none" style="width:100%;height:250px">
      <q-card-section>
        <div class="row">
          <div class="col-12 text-center">
            <div class="q-pb-md">here are the best charging stations nearby:</div>
            <q-scroll-area style="height: 320px;">
              <q-list separator>
                <q-item clickable v-ripple v-for="(station, index) in recommendedPoints" :key="index">
                  <q-item-section @click="centerOnMarker(index)">
                    <q-item-label>{{ station.location_friendlyname }}</q-item-label>
                    <q-item-label caption>{{ station.geocode_string.replace(station.location_friendlyname + ',', '')
                    }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <q-item-label caption>{{ humanTimeSuggestion(station.ds_hour) }}</q-item-label>
                  </q-item-section>
                  <q-item-section side>
                    <NuxtLink :to="'https://www.google.com/maps/dir/?api=1&origin='+userLocation.lat+','+userLocation.lng+'&destination='+station.lat+','+station.lon"><q-btn flat icon="directions"></q-btn></NuxtLink>
                  </q-item-section>
                </q-item>
              </q-list>
            </q-scroll-area>
          </div>
        </div>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-card v-if="loading" class="q-pa-md" flat
    style="width:70%;position:absolute;top:30%;left:50%;transform:translateX(-50%);z-index:1000;background: rgba(255, 255, 255, 0)">
    <div class="row items-center">
      <div class="col-12 text-center">
        <q-circular-progress indeterminate size="150px" :thickness="0.6" color="lime" center-color="grey-8"
          class="q-ma-md" />
      </div>
    </div>
  </q-card>

  <q-dialog v-model="rateDialog">
    <q-card>
      <q-card-section>
        <div class="text-body1">How do you rate my recommendation?</div>
      </q-card-section>

      <q-card-section class="q-pt-none text-center">
        <q-rating v-model="rating" size="3.5em" color="green-5" /> </q-card-section>
      <q-card-actions align="right">
        <q-btn flat label="OK" color="green" v-close-popup @click="reset" />
      </q-card-actions>
    </q-card>
  </q-dialog>


  <q-dialog v-model="stationInfoDialog" seamless position="top">
    <div class="row" style="height:60px"></div>
    <q-card style="width: 350px">

      <q-card-section class="row items-center no-wrap">
        <div>
          <div class="text-weight-bold">{{ selectedStation.location_friendlyname }}</div>
          <div class="text-grey">Suggested charging time: {{ suggestedTimeString(selectedStation.ds) }}</div>
          <div class="text-grey">expect {{ humanUtilization(selectedStation.forecasted_utilization) }} demand</div>
        </div>

        <q-space />


        <q-btn flat round icon="close" v-close-popup />
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<script setup>
import "leaflet/dist/leaflet.css"
import L from "leaflet"
import "leaflet-providers"
import 'leaflet.gridlayer.googlemutant/dist/Leaflet.GoogleMutant.js'
import mapstyle from "../utilities/mapstyle.json"
import flexpolyline from '../assets/flexpolyline';
import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'

const home = ref(true)
const getLocationDialog = ref(true)
const locatingDialog = ref(false)
const getMaximumDistanceDialog = ref(false)
const selectLocationOnMapDialog = ref(false)
const selectChargingTimeDialog = ref(false)
const loadingDialog = ref(false)
const loading = ref(false)
const showRecommendationsDialog = ref(false)
const rateDialog = ref(false)
const maximumChargingPointDistance = ref(5)


const selectedStation = ref()
const stationInfoDialog = ref(false)

const recommendedPoints = ref([])
const rating = ref(0)

var map
var markerArray
var highlightmarker
var bounds = new L.LatLngBounds()
var geojsons = [];
var geoJSONLayer
var getLocationMarker
var userLocationMarker
const userLocation = ref()
const userAddress = ref('')
const selectedPolygon = ref('')

const chargingTime = new Date();
chargingTime.setMilliseconds(0);
chargingTime.setSeconds(0);
const currentMinutes = chargingTime.getMinutes();
const remainder = currentMinutes % 15;
const minutesToAdd = remainder === 0 ? 15 : 15 - remainder;
chargingTime.setMinutes(currentMinutes + minutesToAdd);

const selectedTime = ref({
  hours: chargingTime.getHours(),
  minutes: chargingTime.getMinutes()
});

onMounted(() => {
  initMap()
})


function initMap() {
  map = L.map("map", { zoomControl: false }).setView([45.815399, 15.966568], 12)
  L.gridLayer.googleMutant({
    type: 'roadmap',
    //styles: mapstyle
  }).addTo(map)
  markerArray = L.layerGroup().addTo(map)
  geoJSONLayer = L.geoJSON().addTo(map)
  geoJSONLayer.options.style = {
    "color": "rgba(255,0,0,0.4)",
    "weight": 3,
    "opacity": 0.6
  }
}


function geoLocateUser() {
  const successCallback = (position) => {
    userLocation.value = { lat: position.coords.latitude, lng: position.coords.longitude}
    loading.value = false
    locatingDialog.value = false
    confirmLocation()
  };

  home.value = false
  getLocationDialog.value = false
  loading.value = true
  locatingDialog.value = true
  navigator.geolocation.getCurrentPosition(successCallback);
}

function selectLocationOnMap() {
  home.value = false
  getLocationDialog.value = false
  selectLocationOnMapDialog.value = true
  getLocationMarker = L.marker(map.getCenter(), {
    //draggable: true
  }).addTo(map);
  userLocation.value = map.getCenter()
  function updateMarkerPosition() {
    var center = map.getCenter();
    getLocationMarker.setLatLng(center);
    userLocation.value = map.getCenter()
  }

  onDragEnd()

  async function onDragEnd() {
    var center = map.getCenter();
    const geocoder = new google.maps.Geocoder();
    geocoder
      .geocode({ location: center })
      .then((response) => { userAddress.value = response['results'][0]['formatted_address'] })
  }

  map.on('drag', updateMarkerPosition);
  map.on('move', updateMarkerPosition);
  map.on('moveend', onDragEnd);

}

function confirmLocation() {
  selectLocationOnMapDialog.value = false
  
  if (getLocationMarker) {
    getLocationMarker.removeFrom(map)
  }
  
  userLocationMarker = L.marker(userLocation.value, {
  }).addTo(map);
  getIsolines()
  getMaximumDistanceDialog.value = true
}

function getChargingTime() {
  getMaximumDistanceDialog.value = false
  selectChargingTimeDialog.value = true
}

async function getRecommendation() {

  var polyArray = Object.values(geoJSONLayer._layers)[0]._latlngs
  const coordinatesArray = polyArray[0].map(({ lat, lng }) => [lng.toFixed(3), lat.toFixed(3)])
  coordinatesArray.push([...coordinatesArray[0]])
  var postGISpoly = JSON.stringify({
    type: "Polygon",
    coordinates: [coordinatesArray]
  }, null, 2);

  const { data } = await useFetch('https://www.ai4cs.eu/api/getRecommendation', {
    method: 'POST',
    body: {
      postGISpoly: postGISpoly,
      hour: selectedTime.value.hours.toString()
    },
    onRequest({ request, options }) {
      selectChargingTimeDialog.value = false
      loading.value = true
      loadingDialog.value = true
    },
    onResponse({ request, response, options }) {
      loading.value = false
      loadingDialog.value = false
      recommendedPoints.value = response._data
      console.log(recommendedPoints.value)
      renderRecommendation(response._data)
    }
  })

}

function getEVMarker(clr) {
  return L.divIcon({
    html: `
             <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 100 100">
             <!-- Circle -->
             <circle cx="50" cy="50" r="30" fill="${clr}" />
             <!-- Thunderbolt -->
             <path d="M45,30 L55,50 L40,50 L50,70" fill="yellow" stroke="yellow" stroke-width="6" />
             </svg>
           `,
    className: "",
    iconSize: [48, 48],
    iconAnchor: [24, 24],
  })
}

function getRecommendationDonut(markerData) {
  var hour = parseInt(markerData.ds_hour)
  const colorArray = markerData.donut_data.split(',').map(char => {
    switch (char) {
      case '0':
        return '#009BFF';
      case '1':
        return '#FFD500';
      case '2':
        return '#FF4343';
      default:
        return '#009BFF';
    }
  });
  var arcString = '';
  let startAngle = 0;
  for (let i = 0; i < 24; i++) {
    const endAngle = startAngle + 360 / 24;
    const startX = 50 + 35 * Math.cos((startAngle - 90) * (Math.PI / 180));
    const startY = 50 + 35 * Math.sin((startAngle - 90) * (Math.PI / 180));
    const endX = 50 + 35 * Math.cos((endAngle - 90) * (Math.PI / 180));
    const endY = 50 + 35 * Math.sin((endAngle - 90) * (Math.PI / 180));
    var pathString = `M ${startX} ${startY} A 35 35 0 0 1 ${endX} ${endY}`;
    arcString = arcString + '<path d="' + pathString + '" stroke-width="20" stroke="' + colorArray[i] + '"/>';
    startAngle = endAngle;
  }
  arcString = arcString + `
  <line x1="50" y1="25" x2="50" y2="5" stroke="white" stroke-width="8" stroke-linecap="round" transform="rotate(${hour * 30}, 50, 50)" />
  `
  var size = 64;
  const donut = L.divIcon({
    html: '<svg xmlns="http://www.w3.org/2000/svg" width="' + size + '" height="' + size + '" viewBox="0 0 100 100">' + arcString + '</svg>',
    className: "",
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
  });

  return donut;
}

function renderRecommendation(data) {
  geoJSONLayer.clearLayers()
  markerArray.clearLayers()
  data.forEach(function (markerData, i) {
    //console.log(markerData)
    var clr = 'green'
    var marker = L.marker([markerData.lat, markerData.lon], { icon: getEVMarker(clr) })
      .on('click', (e) => { centerOnMarker(i) })
      .addTo(markerArray)
    bounds.extend(marker.getLatLng());
  });
  //map.fitBounds(bounds);

  showRecommendationsDialog.value = true

}

function highlightStation(e, markerData) {
  if (highlightmarker != undefined) {
    map.removeLayer(highlightmarker);
  }
  highlightmarker = L.marker([markerData.lat, markerData.lon], { icon: getRecommendationDonut(markerData) }).addTo(map)
  selectedStation.value = markerData
  stationInfoDialog.value = true
}

function centerOnMarker(i) {
  map.panTo(new L.LatLng(recommendedPoints.value[i].lat, recommendedPoints.value[i].lon))
  highlightStation(null, recommendedPoints.value[i])
}

async function getIsolines() {
  const { data, pending, error, refresh } = await useFetch(`https://isoline.router.hereapi.com/v8/isolines?transportMode=car&origin=${userLocation.value.lat},${userLocation.value.lng}&range[type]=distance&range[values]=5000,10000,15000,20000,25000,30000,35000,40000,45000,50000,55000,60000&apiKey=wqvPrb-s_609JDBaTKC9eka0KFLW7-OXpVRTJK5Bn3I`)
  var isolines = data._value.isolines


  isolines.forEach((isoline, index) => {

    const polygon = flexpolyline.decode(isoline.polygons[0].outer).polyline;
    const coordinates = polygon.map(([lat, lng]) => [lng, lat]);
    const geojson = {
      type: "FeatureCollection",
      features: [
        {
          type: "Feature",
          geometry: {
            type: "Polygon",
            coordinates: [coordinates]
          },
          properties: {
            id: 1,
            name: "one"
          }
        }
      ]
    };
    const geojson_str = JSON.stringify(geojson);
    geojsons.push(geojson_str);
  });
  geoJSONLayer.clearLayers()
  geoJSONLayer.addData(JSON.parse(geojsons[0]));
  map.fitBounds(geoJSONLayer.getBounds())
}

watch(maximumChargingPointDistance, (v) => {
  geoJSONLayer.clearLayers()
  var distances = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
  geoJSONLayer.addData(JSON.parse(geojsons[distances.indexOf(v)]));
  map.fitBounds(geoJSONLayer.getBounds())
})


function reset() {
  reloadNuxtApp({
    path: "/",
    ttl: 1000, // default 10000
  });
}

function suggestedTimeString(str) {
  var dateString = "2023-07-01 19:00:00";
  var date = new Date(dateString);
  var newHour = date.getHours() + 1;
  date.setHours(newHour);
  var formattedOriginalTime = date.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' });
  date.setHours(newHour + 1);
  var formattedOneHourLater = date.toLocaleTimeString('en-US', { hour12: false, hour: '2-digit', minute: '2-digit' });
  return formattedOriginalTime + ' - ' + formattedOneHourLater
}

function humanUtilization(u) {
  if (u <= 5) { return 'low' }
  if (u > 5 && u <= 20) { return 'medium' }
  if (u > 20) { return 'high' }
}

function humanTimeSuggestion(t) {
  const d = new Date();
  let now_hour = d.getHours();
  if (t-now_hour<1) { return 'now'}
  if (t-now_hour==1) { 'in 1 hour'}
  if (t-now_hour>1) { return 'in ' + (t - now_hour)+ ' hours'}
}
</script>

<style>
body {
  padding: 0;
  margin: 0;
}

#map {
  height: 100%;
  width: 100vw;
}

html,
body {
  height: 100%;
  width: 100vw;
}
</style>