<template>
    <div class="w-100 h-100">
        <l-map ref="map" v-model:zoom="zoom" :center="center" :options="{ zoomControl: false }">
            <l-tile-layer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="© OpenStreetMap contributors" layer-type="base" name="OpenStreetMap"></l-tile-layer>
            <l-marker :lat-lng="markerLatLng"></l-marker>
            <l-polyline :lat-lngs="polylinePoints"></l-polyline> <!-- Add this line -->
            <l-control-attribution :options="{ position: 'topleft' }"></l-control-attribution>
        </l-map>
    </div>
</template>

  
<script lang="ts">
import { defineComponent, ref, watch, type PropType, type Ref } from 'vue';
import "leaflet/dist/leaflet.css";
import "leaflet";
import { LMap, LTileLayer, LMarker, LControlAttribution, LPolyline } from "@vue-leaflet/vue-leaflet";
import type { LatLngExpression, PointExpression } from "leaflet";

export default defineComponent({
    props: {
        markerLatLng: {
            type: Array as unknown as PropType<LatLngExpression>,
            required: true
        },
        routeInput: {
            type: Array,
            required: false
        }
    },
    components: {
        LMap,
        LTileLayer,
        LMarker,
        LControlAttribution,
        LPolyline // Add this line
    },
    setup(props) {
        const zoom = ref(16);
        const center: Ref<PointExpression> = ref([46.4217242, 15.8731548] as PointExpression);
        const inputArray: any[] = [...props.routeInput ? props.routeInput : []];

        const polylinePoints: Ref<Array<LatLngExpression>> = ref([ // Add this line
            ...inputArray.map(point => [point.lat, point.lon]) as unknown as LatLngExpression[]
        ]); // Add this line

        watch(() => props.markerLatLng, (newVal) => {
            const val = newVal as unknown as PointExpression;
            center.value = val;
        });

        watch(() => props.routeInput, (newVal) => {
            const val = newVal as unknown as Array<any>;
            polylinePoints.value = [
                ...val.map(point => [point.lat, point.lon]) as unknown as LatLngExpression[]
            ];
        });

        return {
            zoom,
            center,
            polylinePoints // Add this line
        };
    }
});
</script>
  
<style>
.leaflet-control-attribution.leaflet-control a svg {
    display: none !important;
}

.leaflet-bottom {
    display: none !important;
}
</style>
  