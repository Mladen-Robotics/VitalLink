<script>
import ExitProfileButton from './ExitProfileButton.vue'

import ProfileInfo from './ProfileInfo.vue'
export default {
    components: {
        ExitProfileButton,
        ProfileInfo
    }
}
</script>
<template>
    <main>
   <ProfileInfo />
    <ExitProfileButton />
</main>
</template>
<style scoped>
main {
    display: flex;
    justify-content: space-between;
    padding: 1rem 1rem;
    background: lightblue;
}
</style>