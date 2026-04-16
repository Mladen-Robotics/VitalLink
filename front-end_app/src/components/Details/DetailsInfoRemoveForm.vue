<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

export default {
    props: ["id",],
    data() {
        return {
            errorStatus: false,
        }
    }, methods: {
        async submitRemove() {
            const path = `http://localhost:5000/remove_patient/${this.id}`;

            try {
                const response = axios.get(path);
                this.errorStatus = false;
                this.$emit("patientDeleted");
            } catch(error) {
                console.error("Patient couldn't be deleted: " + error);
                this.errorStatus = true;
            }
        }
    }
}
</script>
<template>
    <form action="#">
    <h1 v-if="errorStatus" class="errorMessage">Couldn't remove patient</h1>

        <h1>Изтриване на пациент</h1>
        <p>Сигурни ли сте, че искате да изтриете пациента?</p>
        <div class="buttons-container">
            <button @click="$emit('closeRemoveForm')" class="info-cancel" type="button">Отказ</button>
            <button @click="submitRemove" class="info-submit" type="button">Изтриване</button>
        </div>
    </form>
</template>
<style scoped>
.errorMessage {
    color: rgb(226, 7, 7);
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

form {
    background: #fff;
    padding: 1rem 2rem;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    box-shadow: 2px 5px 10px 20000px rgba(0, 0, 0, 0.2);
    /* width: clamp(350px, 40%, 400px); */
}

.buttons-container{
    display: flex;
    gap: 3rem;
    margin-bottom: 0.5rem;
    margin-top: 1rem;
}

.buttons-container button {
    padding: 0.5rem 1rem;
    border: none;
    outline: none;
    border-radius: 5px;
    font-weight: 600;
    cursor: pointer;
}

.info-submit {
    background: rgb(226, 7, 7);;
    color: #fff;
}

.info-cancel {
    background: green;
    color: #fff;
}
</style>