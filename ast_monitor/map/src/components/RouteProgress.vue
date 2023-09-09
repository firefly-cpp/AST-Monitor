<template>
    <div class="row h-100">
        <div class="col-8 p-0 text-center d-flex justify-content-center align-items-center">
            <div>
                <h6>To go</h6>
                <div class="border-bottom border-top pb-2 pt-2">
                    <div><span><small>Distance</small></span></div>
                    <v-icon scale="1.5" name="fa-flag-checkered"></v-icon>
                    <div>{{ remainingDistance }} <i><small>km</small></i></div>
                </div>
                <div class="border-bottom border-top pb-2 pt-2">
                    <div><span><small>Ascent</small></span></div>
                    <v-icon scale="1.5" name="fa-mountain"></v-icon>
                    <div>{{ remainingAscent }} <i><small>m</small></i></div>
                </div>
            </div>
        </div>
        <div class="col-4 p-0 m-0 progress-container border border-3 rounded">
            <div class="progress-bar rounded" id="progressBar"></div>
            <div class="text-center w-100 h-100 center-text-flex"
                style="z-index: 99999; position: absolute; display: flex; justify-content: center; flex-direction: column;">
                <div class="row m-0 p-0">%</div>
                <div class="row m-0 p-0">{{ progress }}</div>
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
import { watch, onMounted } from 'vue';



export default {
    props: {
        progress: {
            type: Number,
            default: 0
        },
        remainingDistance: {
            type: Number,
            default: 0
        },
        remainingAscent: {
            type: Number,
            default: 0
        },
    },
    setup(props) {
        const updateProgressBar = () => {
            const progressBar = document.getElementById('progressBar');
            if (progressBar) {
                progressBar.style.height = `${props.progress}%`;
            }
        };

        // Watch for changes to the 'progress' prop
        watch(
            () => props.progress,
            () => {
                updateProgressBar();
            }
        );

        // Initialize the progress bar when the component mounts
        onMounted(() => {
            updateProgressBar();
        });
    }
};

</script>

  
<style scoped>
.progress-container {
    width: 2rem;
    height: 100%;
    background-color: #f3f3f3;
    position: relative;
    box-sizing: border-box;
    /* Include border in the element's total width and height */
}

.progress-bar {
    width: 100%;
    /* Set to 100% to fill the container */
    background-color: rgb(144, 195, 144);
    position: absolute;
    bottom: 0;
    transition: height 0.5s;
    box-sizing: border-box;
    /* Include border in the element's total width and height */
}

.center-text-flex {
    display: flex;
    justify-content: center;
    align-items: center;
}
</style>
  