<template>
    <div class="row m-0 align-items-center p-0" style="height: 15vh;">
        <DisplayCard type="Speed" :value="speed" unit="km/h" />
        <DisplayCard type="Heartrate" :value="heartrate" unit="bpm" />
        <DisplayCard type="Distance" :value="distance" unit="km" />
        <DisplayCard type="Ascent" :value="ascent" unit="m" />
        <DisplayCard type="Duration" :value="duration" unit="" />
    </div>
</template>
  
<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import DisplayCard from './DisplayCard.vue';

export default defineComponent({
    components: {
        DisplayCard,
    },
    props: {
        speed: {
            type: Number,
            default: 0,
        },
        heartrate: {
            type: Number,
            default: 0,
        },
        distance: {
            type: Number,
            default: 0,
        },
        ascent: {
            type: Number,
            default: 0,
        },
        duration: {
            type: String,
            default: '00:00:00',
        },
    },
});
</script>

<style scoped></style>
  