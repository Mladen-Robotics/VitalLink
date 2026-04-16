<script>
export default {
    props: ['name', 'description', 'room'],
}
</script>
<template>
    <main>
    <h1 class="name">
        {{ this.name }}
    </h1>
    <p class="description">
        <!-- Lorem ipsum dolor sit amet consectetur adipisicing elit. Fugiat rerum labore eveniet accusantium aspernatur laborum voluptates, tempora, itaque nobis corporis laudantium aut ab cumque dolores optio dolorem? Architecto, libero repudiandae. -->
        {{ this.description }}
    </p>
    <p class="room">
        Стая: {{ this.room }}
    </p>
    </main>
</template>
<style scoped>
main {
    background: lightgray;
}
/* .description {
    white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
} */
main {
    background: lightgray;
    padding: 16px;
    border-radius: 8px;
    overflow: hidden;
}

.name {
    font-size: 2.2rem;
    font-weight: bold;
    margin-bottom: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.description {
    font-size: 1.8rem;
    color: #2b2b2b;
    font-weight: 600;
    white-space: nowrap; /* Prevent text from wrapping */
    overflow: hidden; /* Hide overflowing text */
    text-overflow: ellipsis; /* Add ellipsis (...) for overflowing text */
}

.room {
    font-size: 1.5rem;
    font-weight: 600;
    color: #464646;
}
</style>