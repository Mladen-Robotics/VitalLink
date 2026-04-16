<script>
import CardPatientInfo from "./CardPatientInfo.vue"

import DetailsButton from "../../Universal/DetailsButton.vue"

import CardChart from "../../Universal/Chart.vue"

import PinnedButtonSmall from "./PinnedButtonSmall.vue"

export default {
    props: ['name', 'description', 'room', 'id'],
    components: {
        CardPatientInfo,
        CardChart,
        DetailsButton,
        PinnedButtonSmall,
    }
}
</script>
<template>
    <main>
        <DetailsButton class="details_button" :id="id" />
        <div class="info-pinbutton-container">
            <div class="pinned-button-small-wrapper">
        <PinnedButtonSmall @patientPinChange="$emit('patientPinChange')" @pinError="$emit('pinError');" :id="id" />
    </div>
        <CardPatientInfo
    :name="name" 
  :description="description" 
  :room="room" 
    />
</div>
    <CardChart :id="id" />
</main>
</template>
<style scoped>

.info-pinbutton-container {
    display: flex;
    align-items: flex-start;
    padding: 0 1rem;
}
main {
    background: lightgray;
    position: relative;
}

.details_button {
    position: absolute;
    top: 1rem;
    right: 1rem;
    z-index: 10;
}

.pinned-button-small-wrapper{
    margin-top: 2rem;
}
</style>