<script>
import SearchInput from './SearchInput.vue'
import FilterButton from './FilterButton.vue'

export default {
    components: {
        SearchInput,
        FilterButton,
    }, 
    data() {
        return {
            name: "",
            description: "",
            room: "",
            path: "",
        }
    },
    computed: {
        generatePath() {
            let path;
            if(this.name == "" && this.description=="" && this.room=="") {
                path = "http://localhost:5000/patient/info?all=True";
            } else {
                path = `http://localhost:5000/patient/info?${this.name!="" ? "name="+this.name: ""}${this.description!="" ? "&description="+this.description : ""}${this.room!="" ? "&room_num="+this.room : ""}`;
            }
            // console.log(path);
            // alert(path)
            return path;
        }
        // async searchPatients() {
        //     const path = this.generatePath();
            
        //     try {
        //         const response = await axios.get(path);
        //         this.data = response.data;
        //         console.log("Data updated:", this.data);
        //     } catch(error) {
        //         console.error("The patients data couldn't be loaded: " + error);
        //     }
        // }
    },
    methods: {
            setPath() {
                this.path = this.generatePath;
                // alert(this.path)
                this.$emit('refreshTable', this.path);
        //         console.log("Setting path...");
        // const path = this.generatePath;
        // console.log("New path:", path);
        // this.path = path;
        // console.log("Path updated to:", this.path);
            }
        },
    mounted() {
        this.setPath;
        this.$emit('refreshTable', "http://localhost:5000/patient/info?all=True");
        // Load all patients on initial mount
        // this.generatePath;
    }
}
</script>

<template>
    <main>
        <SearchInput 
            v-model="name" 
            title="name"
            type="text" 
            placeholder="Име"
            @updateSearchInputValue="(value) => this.name=value"
            />
            
        <SearchInput 
            v-model="description"
            title="description"
            type="text" 
            placeholder="Описание"
            @updateSearchInputValue="(value) => this.description=value"
            />
        <SearchInput 
            v-model="room"
            title="room"
            type="number" 
            placeholder="Стая"
            @updateSearchInputValue="(value) => this.room=value"
            />
        
        <FilterButton @filterButtonClicked="setPath()" />
    </main>
</template>

<style scoped>
main {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin: 2rem 0;
}
</style>