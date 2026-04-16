<script>
import axios from 'axios';
axios.defaults.withCredentials = true;

export default {
  props: ["path",],
  data() {
    return {
      data: {},
      showError: false,
      errorMessage: ''
    }
  }, watch:{
  async path() {
    await this.getData()
    console.log("№№№№№№№№")
    console.log(this.data.error)

    if(this.data.hasOwnProperty('error')) {
      this.showError = true;
      this.errorMessage = "Няма налични резултати от филтрите"
    } else if(Object.keys(this.data)==0) {
      this.showError = true;
      this.errorMessage = "Няма налични повиквания"
    } else {
      this.showErorr = false;
    }
  }
}, methods: {
  async getData() {
    try {
   
      const response = await axios.get(this.path);
      // console.log(response);
      this.data = response.data;
    console.log(this.data.error)
    } catch(error) {
      console.error("Patient calls couldn't be fetched: " + error);
    }
  }
}, mounted() {
  this.showError = false;
}, methods: {
  dataNotConfirmed(rawData) {
    let rawDataEdited = JSON.parse(JSON.stringify(rawData));
    let data = [];
    for(let i=0; i < Object.keys(rawDataEdited); i++) {
      if(rawDataEdited[i].confirmed==0) {
        data.push(rawDataEdited[i]);
      }
    }
    console.log("******************")
    console.log(JSON.parse(JSON.stringify(rawData)));
    return data;
  }
}
}
</script>

<template>
  {{ path[0] }}
  <h1 v-if="showError" class="error-message">{{ errorMessage }}</h1>
  {{ data }}

  <table v-if="data">
    <tr>
      <th>Тип</th>
      <th>Дата/време</th>
      <th>Статус</th>
    </tr>
    <tr v-for="row in dataNotConfirmed(this.data)">
      <td>{{ row.type }}</td>
      <td>{{ row.timestamp }}</td>
      <td>{{ row.confirmed }}</td>
    </tr>
  </table>
</template>

<style scoped>
.error-message {
  color: red;
  font-size: 1.5rem;
  background: rgb(255, 230, 230);
  text-align: center;
  padding: 1rem 0;
}
</style>