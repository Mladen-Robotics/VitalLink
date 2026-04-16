<script>
import axios from 'axios';
axios.defaults.withCredentials = true;


export default {
  props: ["name", "description", "room", "id",],
  data() {
    return {
      nameValue: this.name,
      descriptionValue: this.description,
      roomValue: this.room,
      nameFocused: false,
      descriptionFocused: false,
      roomFocused: false,
      errorStatus: false,
    }
  },
  watch: {
    name(newVal) { this.nameValue = newVal; },
    description(newVal) { this.descriptionValue = newVal; },
    room(newVal) { this.roomValue = newVal; }
  },
  computed: {
    checkChangesComp() {
        if(this.name == this.nameValue && this.description == this.descriptionValue && this.room == this.roomValue) {
            return true;
        }

        if(this.nameValue.trim()==""||this.descriptionValue.trim()==""||String(this.roomValue).trim()=="") {
            return true;
        }
        return false;
    }
  }, methods: {
    async submitChanges() {
        const path = `http://localhost:5000/patient/${this.id}/edit?name=${this.nameValue}&&description=${this.descriptionValue}&&room_num=${this.roomValue}`;

        try {
            const response = await axios.get(path);
            console.log(response.data);
            this.$emit("infoUpdated");
            this.errorStatus = false;
        } catch(error) {
            console.error("Couldn't update data: " + error);
            // alert("Here error");
            this.errorStatus = true;
            this.$emit("infoUpdateError");
        }
    }
  }, nounted() {
    this.errorStatus = false;
  }
}
</script>

<template>
  <form @submit.prevent>
    <h1 v-if="errorStatus" class="errorMessage">Couldn't update data</h1>
    <h1>Редактиране</h1>
    <div class="input-wrappers-container">
      <div
        class="input-wrapper"
        :class="{ floatLabel: nameFocused || nameValue }"
      >
        <p>Име</p>
        <input
          v-model="nameValue"
          type="text"
          @focus="nameFocused = true"
          @blur="nameFocused = false"
        />
      </div>
      <div
        class="input-wrapper"
        :class="{ floatLabel: descriptionFocused || descriptionValue }"
      >
        <p>Описание</p>
        <input
          v-model="descriptionValue"
          type="text"
          @focus="descriptionFocused = true"
          @blur="descriptionFocused = false"
        />
      </div>
      <div
        class="input-wrapper"
        :class="{ floatLabel: roomFocused || String(roomValue) }"
      >
        <p>Стая</p>
        <input
          v-model="roomValue"
          type="number"
          @focus="roomFocused = true"
          @blur="roomFocused = false"
        />
      </div>
    </div>
    <div class="buttons-container">
        <button @click="$emit('closeEditForm')" class="info-cancel" type="button">Отказ</button>
        <button @click="submitChanges" class="info-submit" type="button" :class='{disabledButton: checkChangesComp}'>Потвърждаване</button>
    </div>
  </form>
</template>

<style scoped>
.errorMessage {
    color: rgb(226, 7, 7);
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.disabledButton {
    pointer-events: none;
}

.info-submit.disabledButton {
    background: rgb(81, 182, 123);
}

form {
    display: flex;
    flex-direction: column;
    align-items: center;
    background: #fff;
    padding: 1rem 0rem;
    border-radius: 10px;
    box-shadow: 2px 5px 10px 20000px rgba(0, 0, 0, 0.2);
    width: clamp(350px, 40%, 400px);
}

.input-wrappers-container{
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 2rem 2rem;
    /* background: green; */
    width: 100%;
}

.input-wrapper {
  position: relative;
  height: 3rem;
  border: 2px solid green;
  border-radius: 5px;
  margin-bottom: 1rem;
}

.input-wrapper input {
    width: 100%;
    height: 100%;
    border: none;
    outline: none;
    background: transparent;
    padding: 0 10px;
}

.input-wrapper p {
  position: absolute;
  left: 5px;
  top: 50%;
  transform: translateY(-50%);
  transition: 0.2s;
  color: #888;
  pointer-events: none;
  background: #fff;
  padding: 0 5px;
}

.input-wrapper.floatLabel p {
  top: -15px;
  font-size: 0.9rem;
  color: green;
  background: #fff;
  transform: none;
}
.buttons-container{
    display: flex;
    gap: 4rem;
    margin-bottom: 0.5rem;
}

.buttons-container button {
    padding: 0.5rem 1rem;
    border: none;
    outline: none;
    border-radius: 5px;
    font-weight: 600;
    cursor: pointer;
}

.info-submit {
    background: green;
    color: #fff;
}

.info-cancel {
    background: rgb(226, 7, 7);
    color: #fff;
}

</style>