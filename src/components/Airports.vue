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
  data () {
    return {
      info: null,
      loading: true,
      errored: false
    }
  },
  mounted () {
    axios.defaults.withCredentials = true;
    axios
    .get('../assets/airports.json')
    .then(response => {
      this.info = response
    })}
  }
  </script>