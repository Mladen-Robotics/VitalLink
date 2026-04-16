<script>
import SearchFilters from './DetailsCallsFilters.vue'

import DetailsTable from './DetailsTable.vue'
export default {
    props: ["id",],
    components: {
        SearchFilters,
        DetailsTable,
    }, data() {
        return {
            path: '',
        }
    }
}
</script>
<template>
    {{ path }}
<SearchFilters @refreshTable="(data)=>this.path=data" :id="id" />
<DetailsTable v-if="path" :path="path"/>
</template>
<style scoped>

</style>