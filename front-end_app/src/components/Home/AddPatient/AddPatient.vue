<script>
import AddButton from './AddButton.vue'
import AddForm from './AddForm.vue'

export default {
    components: {
        AddButton,
        AddForm,
    }, data() {
    return {
        state: false,
    }
    }
}
</script>

<template>
{{ state }}
    <AddButton @openAddForm="this.state=true" />
    <AddForm />
</template>

<style scoped>

</style>