<script>
import axios from 'axios'
axios.defaults.withCredentials = true;

export default {
    props: ["id",],
    methods: {
        async unpinPatient() {
            const path = `http://localhost:5000/patient/${this.id}/edit?pinned=False`;
            
            try {
                const response = await axios.get(path);
            console.log("_________________");
            console.log(response.data);
            this.$emit("patientPinChange");
            } catch(error) {
                console.log("Patient couldn't be unpinned: " + error);
                this.$emit("pinError");
            }
        } 
    }
}
</script>
<template>
    <button @click="unpinPatient()" title="Откачване на пациент">
        <img src="../../../assets/unpin_icon.png" alt="">
    </button>
</template>
<style scoped>
button {
    padding: 0.8rem;
    border-radius: 5000px;
    border: none;
    outline: none;
    cursor: pointer;
    position: relative;
    font-weight: 600;
    background: rgb(145, 145, 145);
    transition: background 0.3s;
    width: fit-content;
    display: flex;
    justify-content: center;
    align-items: center;
}
button:hover {
    background: rgb(165, 165, 165);
}
</style>