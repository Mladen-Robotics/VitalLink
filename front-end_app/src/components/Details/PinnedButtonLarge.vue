<script>
import axios from 'axios'
axios.defaults.withCredentials = true;

export default {
    props: ['id', 'pinned'],
    data() {
        return {
            pinnedStatus: this.pinned,
            currentPinCount: null,
            maxPinCount: null,
        }
    }, mounted() {
        this.getData();
    }, methods: {
        async getData() {

            try {
                const path = "http://localhost:5000/patients/pin_count";
                const response = await axios.get(path);
                console.log("^^^^^^^^^^^^^^^^");
                console.log(response.data);
                this.currentPinCount = response.data.count;
            } catch (error) {
                console.error("The current pinned patients count couldn't be fetched: " + error);
                this.$emit("pinError", "The current pinned patients count couldn't be fetched!");
            }

            try {
                const path = "http://localhost:5000/patients/consts/max_pin_count";
                const response = await axios.get(path);
                console.log("((((((((((()))))))))))")
                console.log(response.data);
                this.maxPinCount = response.data;
            } catch (error) {
                console.error("The maximum allowed pinned patients count couldn't be fetched: " + error);
                this.$emit("pinError", "The maximum allowed pinned patients count couldn't be fetched!");
            }
        },
        async pinPatient() {
            const path = `http://localhost:5000/patient/${this.id}/edit?pinned=True`;

            try {
                const response = await axios.get(path);
                console.log("@@@@@@@@@@@")
                console.log(response.data);
                this.currentPinCount++;
                this.pinnedStatus = true;
                this.$emit("patientPinChange");
            } catch (error) {
                console.error("Patient coudn't be pinned: " + error);
                this.$emit("pinError", "Patient couldn't be pinned!");
            }
        }, async unpinPatient() {
            const path = `http://localhost:5000/patient/${this.id}/edit?pinned=False`;

            try {
                const response = await axios.get(path);
                console.log("***********")
                console.log(response.data);
                this.currentPinCount--;
                this.pinnedStatus = false;
                this.$emit("patientPinChange");
            } catch (error) {
                console.error("Patient coudn't be unpinned: " + error);
                this.$emit("pinError", "Patient couldn't be unpinned!");
            }
        },
        handleClick() {
            if (this.pinnedStatus == true) this.unpinPatient();
            else this.pinPatient();
        },
    }, computed: {
        buttonText() {
            if (this.pinnedStatus == true) {
                return "Unpin patient"
            } else if (this.pinnedStatus == false) {
                if (this.currentPinCount < this.maxPinCount) {
                    return "Pin patient"
                } else {
                    return "Maximum pin count of " + this.maxPinCount + " was reached";
                }
            }
        }, buttonStyle() {
            if (this.pinnedStatus == true) {
                return [{ backgroundColor: 'rgb(121,121,121)' }, { color: '#fff' }]
            } else {
                return [{ backgroundColor: 'green' }, { color: '#fff' }]
            }
        },
    }
}

</script>

<template>
    <button :style="buttonStyle" @click="handleClick()"
        :disabled="this.currentPinCount == this.maxPinCount && this.pinnedStatus == false">{{ buttonText }}</button>

</template>

<style scoped>
button {
    padding: 0.5rem 1rem;
    border-radius: 5px;
    border: none;
    outline: none;
    cursor: pointer;
    position: relative;
    font-weight: 600;
    pointer-events: none;
    user-select: none;
}
button:hover::before {
    display: block;
    visibility: visible;
    opacity: 1;
}
button::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 5px;
    background: rgba(0, 0, 0, 0.2);
    top: 0;
    left: 0;
    visibility: none;
    opacity: 0;
    transition: 0.3s;
    pointer-events: all;
}

button:disabled:after {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 5px;
    background: rgba(255,255,255, 0.6);
    top: 0;
    left: 0;
    transition: 0.3s;
    pointer-events: all;
    z-index: 1;
    cursor: not-allowed;
}

button:disabled:hover::before{
opacity: 0;
}
</style>