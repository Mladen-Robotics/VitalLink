<script>
export default {
  props: ['id', 'type', 'placeholder'],
  data() {
    return {
      inputValue: '',
    }
  },
  methods: {
    // getCurrentDateTime() {
    //   const d = new Date();
    //   const year = d.getFullYear();
    //   const month = String(d.getMonth() + 1).padStart(2, '0');
    //   const day = String(d.getDate()).padStart(2, '0');
    //   const hours = String(d.getHours()).padStart(2, '0');
    //   const minutes = String(d.getMinutes()).padStart(2, '0');

    //   // Set value depending on input type
    //    if (this.type === 'date') {
    //     this.inputValue = `${year}-${month}-${day}`;
    //   } else if (this.type === 'time') {
    //     this.inputValue = `${hours}:${minutes}`;
    //   } else {
    //     // For text or other types, use Bulgarian format as an example
    //     this.inputValue = `${day}.${month}.${year} ${hours}:${minutes}`;
    //   }
    // }
  },
  mounted() {
    // this.getCurrentDateTime();
  }, watch: {
    inputValue(newValue) {
       alert("new value: '" + newValue + "'");
      this.$emit("updateSearchInputValue", newValue)
    }
  }
}
</script>

<template>
  <div>
    <input 
      v-model="inputValue"
      :type="type" 
      :placeholder="placeholder"
    >
    <button v-if="this.inputValue!=''" @click="this.inputValue=''">x</button>
  </div>
</template>

<style scoped>
div {
  display: flex;
  align-items: center;
  border: 2px solid green;
  padding: 0 10px;
  border-radius: 10px;
  gap: 10px;

}
input {
  border: none;
  outline: none;
  font-size: 1.2rem;
  height: 2.5rem;
  background: transparent;
}
button {
width: 20px;
border-radius: 50%;
border: none;
outline: none;
color: red;
cursor: pointer;
}
</style>