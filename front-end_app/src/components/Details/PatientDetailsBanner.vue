<script>
import axios from 'axios'
axios.defaults.withCredentials = true;

import PinnedButtonLarge from '../Details/PinnedButtonLarge.vue'

export default {
    props: ['id'],
    components: {
        PinnedButtonLarge,
    },
    data() {
        return {
            name: '',
            description: '',
            room: null,
            pinnedStatus: '',
            showPinnedButtonLarge: false,
            showError: false,
            errorMessage: '',
        }
    }, methods: {
        async getData() {
            try {
                const path = `http://localhost:5000/patient/info?patientID=${this.id}`;

                const response = await axios.get(path)

                console.log(response.data);

                this.name = response.data[0].name;

                this.description = response.data[0].description;

                this.room = response.data[0].room_num;
                this.pinnedStatus = response.data[0].pinned == "True";
                // alert("hello: " + this.pinnedStatus);
                this.showPinnedButtonLarge = true;
            } catch (error) {
                console.error("Data couldn't be fetched: " + error);
            }
        }, handlePinError(msg) {
            this.errorMessage = msg;
            this.showError = true;
        }
    },
    mounted() {
        this.getData();
        this.showError = false;
    },
}
</script>

<template>
    <h1 class="error-message" v-if="showError">{{ errorMessage }}</h1>
    <main>
        <div class="container">
            <div class="patientDetailsContent">
                <h1>{{ name }}</h1>
                <p>
                    {{ description }}
                </p>

                <p>
                    Стая: <b>{{ room }}</b>
                </p>
            </div>
            <PinnedButtonLarge @pinError="handlePinError" @patientPinChange="$router.push('/')"
                v-if="showPinnedButtonLarge" :id="id" :pinned="pinnedStatus" />
        </div>
    </main>



</template>

<style scoped>
.error-message {
    color: red;
    text-align: center;
    background: rgb(255, 230, 230);
    padding: 1rem 0;
}

.container {
    background: #d1d1d1;
    padding: 2rem 1rem;
    display: flex;
    justify-content: space-between;
    /* align-items: flex-start; */
    align-items: center;
    gap: 0.5rem;
}

div {
    /* background: green; */
}
</style>
