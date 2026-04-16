<script>
import FiltersTable from './DetailsCallsFiltersTable.vue'
export default {
    props: ["id",],
    components: {
        FiltersTable,
    },
    data() {
        return {
            
        }
    }
}
</script>
<template>
    <FiltersTable :id="id" />
</template>
<style scoped></style>