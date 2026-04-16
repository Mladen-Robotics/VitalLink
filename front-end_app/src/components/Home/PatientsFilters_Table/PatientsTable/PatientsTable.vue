<script>
import axios from 'axios'
axios.defaults.withCredentials = true;

import DetailsButton from '../../../Universal/DetailsButton.vue'

export default {
  props: ['pathData'],
  components: {
    DetailsButton,
  },
  data() {
    return {
      path: this.pathData,
      data: null,
      noPatientsInDB: true,
      noFilteredRes: false,
    }
  }, watch: {
    pathData(newValue) {
      // alert("---------")
      // alert(newValue);
      console.log("-----------");
      console.log(newValue);
      this.path = newValue;

      if (this.path == "http://localhost:5000/patient/info?all=True") {
        // this.
      }

      this.getData();
    }
  }, methods: {
    async getData() {
      let response;
      try {
        response = await axios.get(this.path);
        console.log("+++++++++++")
        console.log(response.data);
        this.data = response.data;
        console.log("Data updated:", this.data);

      } catch (error) {
        console.error("The patients data couldn't be loaded: " + error);
      }
      console.log(response.data);
      
      console.log(JSON.parse(JSON.stringify(this.data)))
      if (Array.isArray(this.data)) {
        this.noFilteredRes = false;
        if (this.data.length == 0) {
          this.noPatientsInDB = true;
        } else {
          this.noPatientsInDB = false;
        }
      } else if (this.data !== null && typeof this.data === 'object') {
        this.noFilteredRes = true;
        this.noPatientsInDB = false;
      } else {
        console.log("Neither");
      }
      // alert(this.data[0])
    }
  }
}
</script>
<template>
  <main>
  <!-- {{ path }} -->
  <p v-if="noPatientsInDB">Няма налични пациенти</p>
  <p v-if="noFilteredRes">Няма налични резултати от филтрите</p>

  <table v-if="!noPatientsInDB && !noFilteredRes">
    <tr>
    <th>Име</th>
    <th>Описание</th>
    <th>Стая</th>
    <th>Детайли</th>
  </tr>
  <tr v-for="n in JSON.parse(JSON.stringify(this.data)).length" :key="n">
    <td style="font-weight: 600; color: green;">{{ JSON.parse(JSON.stringify(this.data))[n-1].name }}</td>
    <td>{{JSON.parse(JSON.stringify(this.data))[n-1].description}}</td>
    <td>{{JSON.parse(JSON.stringify(this.data))[n-1].room_num}}</td>
    <td>
      <DetailsButton :id="data[n-1].PatientID" />
    </td>
  </tr>
  </table>
</main>
</template>
<style scoped>
main {
  /* background: red; */
  display: flex;
  justify-content: center;
}

p {
  font-size: 1.5rem;
  font-weight: 600;
  color: tomato;
}

table tr{
  padding: 1rem 1rem;
  margin: 1rem;
}

table th {
  padding: 1rem 2rem;
  font-size: 1.5rem;
  background: #d1d1d1;
}

table td {
  padding: 0.5rem 2rem;
  font-size: 1.5rem;
  text-align: center;
  border: none;
}

table tr:nth-child(odd) {
  background-color: #f0f0f0; /* or any gray shade you prefer */
}

  main {
  width: 100%;
  display: flex;
  justify-content: center;
}

table {
  width: 90%;
  max-width: 1320px;
  table-layout: fixed;
}

table th, table td {
  text-align: center;
}

table td:first-child, table th:first-child {
  text-align: center;
}
</style>