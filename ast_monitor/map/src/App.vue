<script setup lang="ts">
import { onMounted, ref } from 'vue';
import RouteProgress from './components/RouteProgress.vue';
import Map from './components/Map.vue';
import DisplayCard from './components/DisplayCard.vue';
import type { LatLngExpression } from 'leaflet';
import TrainingMetrics from './components/TrainingMetrics.vue';
// Define ref to hold each value, initialize with default values
const progress = ref(0);
const remainingDistance = ref(0);
const speed = ref(0);
const heartrate = ref(0);
const duration = ref('00:00:00');
const distance = ref(0);
const mapRef = ref([46.4217242, 15.8731548] as LatLngExpression);
const ascent = ref(5);
const remainingAscent = ref(0);
const routeInput = ref([{ 'id': 297698642, 'lat': 46.4217242, 'lon': 15.8731548 }, { 'id': 5863859668.0, 'lat': 46.4218289, 'lon': 15.873308 }, { 'id': 703743540, 'lat': 46.4218974, 'lon': 15.8733977 }, { 'id': 703743540, 'lat': 46.4218974, 'lon': 15.8733977 }, { 'id': 1589798755, 'lat': 46.4221766, 'lon': 15.8737995 }, { 'id': 1589798755, 'lat': 46.4221766, 'lon': 15.8737995 }, { 'id': 297698681, 'lat': 46.4222396, 'lon': 15.8738768 }]);


// Function to set all values
function setValues(newValues: {
  progress?: number,
  remainingDistance?: number,
  remainingAscent?: number,
  speed?: number,
  heartrate?: number,
  duration?: string,
  distance?: number;
  lat_lng?: LatLngExpression;
  ascent?: number;
  routeInput?: [];
}) {
  if (newValues.progress !== undefined) progress.value = newValues.progress;
  if (newValues.remainingDistance !== undefined) remainingDistance.value = newValues.remainingDistance;
  if (newValues.remainingAscent !== undefined) remainingAscent.value = newValues.remainingAscent;
  if (newValues.speed !== undefined) speed.value = newValues.speed;
  if (newValues.heartrate !== undefined) heartrate.value = newValues.heartrate;
  if (newValues.duration !== undefined) duration.value = newValues.duration;
  if (newValues.distance !== undefined) distance.value = newValues.distance;
  if (newValues.lat_lng !== undefined) mapRef.value = newValues.lat_lng;
  if (newValues.ascent !== undefined) ascent.value = newValues.ascent;
  if (newValues.routeInput !== undefined) routeInput.value = newValues.routeInput;
}




onMounted(() => {
  let w = window as unknown as CustomWindow;
  w.setValues = setValues;
});

export interface CustomWindow extends Window {
  setValues: any;
}

</script>

<template>
  <div class="row m-0 text-center" style="height: 84vh; background-color: rgb(254, 254, 254);">
    <div class="col-10 p-0">
      <Map :route-input="routeInput" :marker-lat-lng="mapRef"></Map>
    </div>
    <div class="col-2 pl-2 ">
      <RouteProgress :progress="progress" :remaining-distance="remainingDistance" :remaining-ascent="remainingAscent">
      </RouteProgress>
    </div>
  </div>
  <div class="row m-0 align-items-center p-0" style="height: 15vh;">
    <TrainingMetrics :speed="speed" :ascent="ascent" :heartrate="heartrate" :distance="distance" :duration="duration">
    </TrainingMetrics>
  </div>
</template>

<style scoped></style>
