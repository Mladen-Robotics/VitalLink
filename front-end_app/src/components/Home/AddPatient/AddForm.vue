<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

export default {
    data() {
        return {
            foundDevices: [],
            foundDevicesCount: "loading",
            selectedDevice: '',
            nameValue: '',
            descriptionValue: '',
            roomValue: '',
            isDisabled: false,
        }
    }, computed: {
        isDisabled() {
            return false;
        }
    }, mounted() {
        this.getCurrentDevices();
        this.checkClickedDevices();
    }, methods: {
        checkClickedDevices() {
            const deviceList = document.querySelectorAll("li");

            deviceList.forEach((device)=>{
                device.addEventListener("click", ()=>{
                    alert("lsdjf")
                    alert(device.getAttribute("value"))
                })
            })
        },
    async getCurrentDevices() {
        const path = `http://localhost:5000/devices/info/presence`;

        try {
            const response = await axios.get(path);
            console.log(response.data);
            this.foundDevices = response.data.devices;
            this.foundDevicesCount = this.foundDevices.length;
        } catch(error) {
            console.error("Found devices data couldn't be fetched: " + error);
        }
    }, handleDeviceClick(device) {
        console.log(device)
        document.querySelectorAll("li").forEach((el)=>{
            el.classList.remove("selected-device")
        })
        alert(device);
        const index = this.foundDevices.indexOf(device);
        document.querySelectorAll("li")[index].classList.add("selected-device");
        this.selectedDevice = device;
    },
    }, watch: {
        isDisabled() {
            if(this.nameValue.trim()==""||this.descriptionValue.trim()==""||String(this.roomValue).trim()==""){
                return false;
            }
            return true;
        }
        // foundDevices(newValue) {
        //     alert(newValue.length)
        //     this.foundDevicesCount = newValue.length;
        //     // for(let i=0; i < newValue.length; i++) {
        //     //     this.foundDevices.push(`Device ${newValue[i]}`);
        //     // }
        // }
    }
}
</script>
<template>
    <main>
        {{ selectedDevice }}
    <form action="#">
        <h1>Добавяне на пациент</h1>
        <input v-model="nameValue" title="Име" placeholder="name" type="text">

        <input v-model="descriptionValue" title="Описание" type="text" placeholder="Описание">
        <input v-model="roomValue" title="Стая" type="number" placeholder="Стая">
        <h3>Намерени устройства ({{ foundDevicesCount }})</h3>
        <div class="available-list-wrapper">
            <ul>
    <li v-for="item in foundDevices" 
        :key="item" 
        :value="item" 
        @click="handleDeviceClick(item)">
        Device {{ item }}
    </li>
</ul>
        </div>
<div class="buttons-wrapper">
        <button class="cancel" type="button">Отказ</button>
        <button :disabled="isDisabled" class="submit" type="button">Добавяне</button>
    </div>
    </form>
</main>
</template>
<style scoped>
.selected-device {
    background: lightgreen;
}

.available-list-wrapper {
/* background: red; */
/* padding: 1rem ; */
width: 100%;
border: 2px solid green;
border-radius: 5px;
max-height: 7.5rem;
overflow: scroll;
}

ul {
    list-style-type: none;
}

li {
    background: lightgray;
    padding: 0.5rem;
    cursor: pointer;
}

li:hover {
    background: rgb(172, 172, 172);
}

main {
    padding: 0 1rem;
    display: flex;
    justify-content: center;
}
form {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    background: #fff;
    width: fit-content;
    padding: 2rem 4rem;
    border-radius: 10px;
    /* box-shadow: 0 0 0px 1000000px rgba(0, 0, 0, 0.6); */
    /* background: green; */
    border: 2px solid green;
    /* width: 50%; */

}
input {
    height: 2.5rem;
    padding: 0 10px;
    border: 2px solid green;
    outline: none;
    border-radius: 5px;
    max-width: 20rem;
}
.buttons-wrapper {
    display: flex;
    gap: 1rem;
}

button {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    border: none;
    outline: none;
    color: #fff;
    font-weight: 600;
    border-radius: 5px;
    cursor: pointer;
}

.cancel {background: rgb(201, 0, 0);}
.submit {background: green;}
</style>