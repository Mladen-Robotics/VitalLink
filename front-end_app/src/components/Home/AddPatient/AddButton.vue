<script></script>
<template>
 <button @click="$emit('openAddForm')"> Добавяне на пациент</button>
</template>
<style scoped>
button{
    padding: 0.5rem 1rem;
    font-size: 1rem;
    border: none;
    outline: none;
    background: green;
    color: #fff;
    font-weight: 600;
    border-radius: 10px;
}
</style>