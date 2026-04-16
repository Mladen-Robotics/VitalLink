<script>
export default {
    props: ['id'],
}
</script>
<template>
    <main>
    <a :href="'patient/'+ this.id">
    <button>
        Детайли
    </button>
</a>
</main>
</template>
<style scoped>
button {
    background: green;
    border: none;
    outline: none;
    padding: 0.5rem 1rem;
    border-radius: 10px;
    font-size: 1.2rem;
    text-decoration: none;
    color: #fff;
    font-weight: 600;
    letter-spacing: 0.5px;
    cursor: pointer;
    transition: background 0.2s;
}

button:hover{
    background: rgb(0, 97, 0);
}
</style>