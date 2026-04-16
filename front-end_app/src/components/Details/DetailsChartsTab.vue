<script>
import Chart from "../Universal/Chart.vue"

export default {
    props: ['id'],
    components: {
        Chart,
    },
    data() {
        return {
            
        }
    }
}
</script>
<template>
    <Chart :id="id" />
</template>
<style scoped></style>