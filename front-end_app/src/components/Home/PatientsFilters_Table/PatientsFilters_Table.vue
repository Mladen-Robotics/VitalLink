<script>
import HomeSearchFilters from './SearchFilters/SearchFilters.vue'

import HomePatientsTable from './PatientsTable/PatientsTable.vue'

export default {
    components: {
        HomeSearchFilters,
        HomePatientsTable,
    },
    methods: {
        refreshTable(res) {
            // alert("Refreshing the table")
            // alert(res)
            this.path = res;
            // alert("#####")
            // alert(this.path)
        }
    }, data() {
        return {
            path: "",
        }
    }
}
</script>
<template>
<HomeSearchFilters @refreshTable="(res) => refreshTable(res)" />
<HomePatientsTable :pathData="path" />
</template>
<style scoped>
.table-filters-wrapper {
  width: 100%;
  max-width: 1200px; /* or any value you want */
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: stretch;
}
</style>