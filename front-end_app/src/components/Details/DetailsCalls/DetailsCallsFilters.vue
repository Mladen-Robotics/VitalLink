<script>
import SearchInput from './SearchInput.vue'
import FilterButton from './FilterButton.vue'
import SearchDropdown from './SearchDropdown.vue'

export default {
    props: ["id",],
    components: {
        SearchInput,
        SearchDropdown,
        FilterButton,
    }, 
    data() {
        return {
            type: "",
            date: "",
            time: "",
            path: "",
        }
    },
    computed: {
        generatePath() {
            let dateArray = this.date.split('-');
            dateArray = dateArray.map((n)=> {return Number(n)})

            let timeArray = this.time.split(':');
            timeArray = timeArray.map(n=>{return Number(n)})

            let path=`http://localhost:5000/patient/${this.id}/notifications?${this.type&&this.type!="all"?`type=${this.type}`:""}${this.date==""?"":`&&day=${dateArray[2]}&&month=${dateArray[1]}&&year=${dateArray[0]}`}${this.time==""?"":`&&hours=${timeArray[0]}&&minutes=${timeArray[1]}`}`;
            
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
                this.$emit('refreshTable', this.path);
        //         console.log("Setting path...");
        // const path = this.generatePath;
        // console.log("New path:", path);
        // this.path = path;
        // console.log("Path updated to:", this.path);
            }
        },
    mounted() {
        this.setPath();

        this.$emit('refreshTable', this.path);
        // Load all patients on initial mount
        // this.generatePath;
    }
}
</script>

<template>
    <main>
        {{ id }}
        {{ type }}
        {{ date }}
        {{ time }}
        <div class="container">
        <SearchDropdown 
            v-model="name" 
            title="тип"
            type="text" 
            placeholder="Тип"
            @changeDropdownValue="(value) => this.type=value"
            />
            <SearchInput 
            v-model="dateTime"
            title="description"
            type="date" 
            placeholder="Описание"
            @updateSearchInputValue="(value) => this.date=value"
            />
            <SearchInput 
            v-model="dateTime"
            title="description"
            type="time" 
            placeholder="Описание"
            @updateSearchInputValue="(value) => this.time=value"
            />
        
        <FilterButton @filterButtonClicked="setPath()" />
    </div>
   </main>
</template>

<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin: 2rem 0;
}
</style>