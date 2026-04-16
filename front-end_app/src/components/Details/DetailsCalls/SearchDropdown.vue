<script>
export default {
  data() {
    return {
      selectedType: "all"
    }
  }, methods: {
    updateValue(event) {
        // alert(event.target.value)
        alert(" ddddd   " + event.target.value)
    }
  }, watch: {
    selectedType(newValue) {
        this.$emit('changeDropdownValue', newValue);
    }
  }, mounted() {
    this.$emit('changeDropdownValue', this.selectedType);
  }
}
</script>

<template>
    <div class="container">
      <select v-model="selectedType" name="type">
        <option value="all">всички</option>
        <option value="ordinary" :style="{ background: 'green', color: 'white' }">обикновени</option>
        <option value="emergency" :style="{ background: 'red', color: 'white' }">спешни</option>
      </select>
    </div>
  </template>

<style scoped>
.container {
  border: 2px solid green;
  outline: none;
  border-radius: 10px;
  padding: 0 5px;
  font-size: 1.2rem;
  width: 15rem;
  height: 2.5rem;
}
select {
  width: 100%;
  height: 100%;
  background: transparent;
  border: none;
  outline: none;
  font-size: 1.2rem;
}
</style>