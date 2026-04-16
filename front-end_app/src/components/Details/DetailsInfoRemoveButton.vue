<script></script>

<template>
    <button @click="$emit('showRemoveForm')">Изтриване на пациент</button>
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
    background: rgb(226, 7, 7);
    color: #fff;
    font-weight: 600;
}

button:hover {
    background: rgb(189, 0, 0);
}
</style>