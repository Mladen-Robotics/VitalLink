<script>
export default {
  props: ['type', 'placeholder', 'modelValue', 'title'],  // Add modelValue prop
  emits: ['updateSearchInputValue'],  // Define the emit event
  methods: {
    validateNumber(event) {
      // Allow only numbers, backspace, delete, tab, arrows, etc.
      const allowedKeys = ['Backspace', 'Delete', 'Tab', 'ArrowLeft', 'ArrowRight', 'Home', 'End'];
      
      // If it's not a number and not an allowed key, prevent the input
      if (!/^\d*$/.test(event.key) && !allowedKeys.includes(event.key)) {
        event.preventDefault();
      }
    },
    updateValue(event) {
      // Emit the new value to the parent
      this.$emit(`updateSearchInputValue`, event.target.value);
    }
  }
}
</script>

<template>
  <input 
    :type="type" 
    :placeholder="placeholder"
    :value="modelValue"
    @input="updateValue"
    @keydown="type === 'number' ? validateNumber($event) : null">
</template>
<style scoped>
input {
    border: 2px solid green;
    outline: none;
    border-radius: 10px;
    padding: 0 10px;
    font-size: 1.2rem;
}
</style>