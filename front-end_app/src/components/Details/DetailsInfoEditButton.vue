<script></script>
<template>
    <main>
    <button @click="$emit('showEditForm')">Редактиране</button>
    </main>
</template>
<style scoped>
button {
    width: fit-content;
    padding: 0.5rem 1rem;
    font-size: 1rem;
    margin-bottom: -1rem;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: background 0.1s;
    background: rgb(221, 221, 221);
}

button:hover {
    background: rgb(192, 192, 192);;
}
</style>