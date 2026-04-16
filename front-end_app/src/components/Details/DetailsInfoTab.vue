<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

import EditButton from '../Details/DetailsInfoEditButton.vue'

import EditForm from '../Details/DetailsInfoEditForm.vue'

import RemoveButton from '../Details/DetailsInfoRemoveButton.vue'

import RemoveForm from '../Details/DetailsInfoRemoveForm.vue'

export default {
    props: ["id"],
    components: {
        EditButton,
        EditForm,
        RemoveButton,
        RemoveForm,
    },
    data() {
        return {
            name: '',
            description: 'Loading',
            room: null,
            showEditForm: false,
            showRemoveForm: false,
        }
    }, methods: {
        async getData() {
            const path = `http://localhost:5000/patient/info?patientID=${this.id}`;

            try {
                const response = await axios.get(path)
                this.name = response.data[0].name;
                this.description = response.data[0].description;
                this.room = response.data[0].room_num;
                console.log("-----------------")
                console.log(response.data[0]);
                
            } catch(error) {
                console.error("Can't fetch data: " + error);
                this.description = "Can't fetch data";
            }

        }
    }, mounted() {
        this.getData();
    }
}
</script>
<template>
    <main>
        <div v-if="showEditForm" class="EditFormWrapper">
        <EditForm @infoUpdateError="alert('Error')" @infoUpdated="this.getData();this.showEditForm=false;$emit('infoUpdated2')" @closeEditForm="this.showEditForm=false" :name="this.name" :description="this.description" :room="this.room" :id="id" />
        </div>
        <div v-if="showRemoveForm" class="RemoveFormWrapper">
        <RemoveForm @patientDeleted="this.showRemoveForm=false; this.$router.push('/')
" @closeRemoveForm="this.showRemoveForm=false" :id="id"/>
    </div>
        
        <div class="details-info-container">
            <div class="infoButtonWrapper">
            <EditButton @showEditForm="showEditForm=true" />
            <RemoveButton @showRemoveForm="showRemoveForm=true" />
            </div>
            <hr>
            <div>
            <span>Име:</span> 
        <h2>
            {{ name }}
        </h2>
    </div>
        <div>
            <span>Описание:</span> 
        <h3>
            {{ description }}
        </h3>
    </div>
    <div>
            <span>Стая:</span> 
        <h3>
            {{ room }}
        </h3>
    </div>
    </div>
    </main>
</template>
<style scoped>

.EditFormWrapper,
.RemoveFormWrapper {
position: absolute;
top: 50%;
left: 50%;
transform: translate(-50%, -50%);
}

main {
    display: flex;
    align-items: center;
}

.details-info-container{
    /* background: green; */
    width: 90%;
    max-width: 1320px;
    border: 4px solid green;
    border-radius: 10px;
    padding: 1rem 2rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.infoButtonWrapper {
    justify-content: space-between;
}

.details-info-container>div {
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 1.2rem;
}

.details-info-container>div span {
    font-size: 1.5rem;
}

</style>