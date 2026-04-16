<script>
import PinnedCard from './PinnedCard.vue';
import axios from 'axios';

axios.defaults.withCredentials = true;

export default {
    components: {
        PinnedCard,
    },
    data() {
        return {
            infoData: {}, // Holds the fetched data
            pinnedCount: 0, // Default value for the number of columns
            showError: false,
        };
    },
    methods: {
        async getInfoData() {
            try {
                const response = await axios.get("http://localhost:5000/patient/info?pinned=True");
                this.infoData = response.data;
                this.pinnedCount = Object.keys(this.infoData).length; // Update pinnedCount
                console.log(this.infoData);
                console.log("+++++++++++++++++++++++++");
                console.log(this.infoData.error!=undefined);
                
                
            } catch (error) {
                console.error('Error fetching user info:', error);
                return null; // Return null if there's an error
            }
        },
    },
    computed: {
        gridColumnsComputed() {
            return `repeat(${this.pinnedCount}, 1fr)`; // Dynamically set grid columns
        },
    },
    mounted() {
        this.getInfoData();
        this.showErorr = false;
    },
};
</script>

<template>
    <div v-if="showError" class="error-message">
        <h1>Пациента не беше откачен успешно!</h1>
    </div>
    <main :style="{ gridTemplateColumns: gridColumnsComputed }">
        <PinnedCard 
            v-for="(item, index) in infoData" 
            :id="item.PatientID"
            :name="item.name" 
            :description="item.description" 
            :room="item.room_num" 
            :key="index" 
            @patientPinChange="getInfoData()"
            @pinError="this.showError=true"
            v-if="this.infoData.error==undefined"
        />
        <div v-if="this.infoData.error!=undefined" class="noPatientsPinned">Няма закачени пациетни</div>
    </main>
</template>

<style scoped>
.error-message {
    color: red;
    text-align: center;
    background: rgb(255, 230, 230);
    padding: 2rem 0;
}

.noPatientsPinned {
    background: lightgray;
    text-align: center;
    padding: 2rem;
    font-size: 2rem;
    margin-bottom: 10rem;
}

main {
    display: grid;
    gap: 10px; /* Add spacing between cards */
    margin-bottom: 5rem;
    /* background: lightgray; */
}
</style>