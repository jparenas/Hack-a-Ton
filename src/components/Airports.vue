<template>
  <div id="app">
    <h1>Airports</h1>
    <div v-for='A in info' v-bind:key='index' id = 'airports'>
      {{ A }}:
      <span>
        <span v-html="aircports-symbol"></span>
      </span>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name:"Airports",
  props:{
  },
  data () {
    return {
      info: null,
      loading: true,
      errored: false
    }
  },
  // filters: {
  //   codefilter (value) {
  //     return value.code
  //   },
  //   namefilter (value) {
  //     return value.name
  //   }
  // },
  mounted () {
    axios.defaults.withCredentials = true;
    axios
    .get('../assets/airports.json')
    .then(response => {
      this.info = response
    })
      // .catch(error => {
      //   // console.log(error)
      //   this.errored = true
      // })
      // .finally(() => this.loading = false)
    }
  }
  </script>