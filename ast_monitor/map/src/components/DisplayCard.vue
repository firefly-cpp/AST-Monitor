<template>
    <div class="col border-start h-100">
        <div class="card p-0 border-0 h-100 bg-white">
            <div class="row card-body d-flex align-items-center text-center">
                <div class="col-4 p-0 text-center align">
                    <i :class="cardIcon" style="font-size: 2rem;"></i>
                </div>
                <div class="col-8 p-0">
                    <h6 class="card-title p-0 m-0" style="font-size: 0.9rem;">{{ type }}</h6>
                    <h5 class="card-text" style="font-size: 1rem;">{{ value }} <i><small>{{ unit }}</small></i></h5>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent, type PropType } from 'vue';
import "bootstrap-icons/font/bootstrap-icons.css";

export default defineComponent({
    props: {
        type: {
            type: String,
            required: true
        },
        value: {
            type: [Number, String],
            required: true
        },
        unit: {
            type: String,
            required: true
        }
    },
    computed: {
        cardIcon(): string {
            switch (this.type) {
                case 'Speed':
                    return 'bi-speedometer';
                case 'Heartrate': ;
                    return 'bi-heart';
                case 'Distance':
                    return 'bi-geo-alt';
                case 'Ascent':
                    return 'bi-arrow-up';
                case 'Duration':
                    return 'bi-clock';
                default:
                    return 'bi-question';
            }
        }
    },


});
</script>
  
<style scoped>
.card {
    padding: 0.0rem;
}

.card-body {
    padding: 0.1rem;
}
</style>
  