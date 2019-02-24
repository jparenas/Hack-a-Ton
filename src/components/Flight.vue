<template>
  <div>
    <h1>Liked ones!</h1>
    <div v-for='f in info' :key='idx' id='flight'>
      {{ f }}:
      <span>
        <span v-html='f.flights'></span>
      </span>
    </div>
    <!-- <div v-for="currency in info" class="currency">
      {{ currency.description }}:
      <span class="lighten">
        <span v-html="currency.symbol"></span>{{ currency.rate_float | currencydecimal }}
      </span>
    </div> -->
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Flight',
  props: {
  },
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
      // .get('http://localhost:8080/api/get_flights?')
      .get('http://localhost:8080/api/get_flights?end_date=2019-03-01&start_date=2019-02-24&budget=500&uuid=1&origin=MAD')
      .then(response => {
        this.info = response
      })
      // .catch(error => {
      //   this.errored = true,
      //   console.log(error)
      // })
      // .finally(() => this.loading = false)
  }
}
</script>

<style>
.flight {
  color: white;
}

h1 {
  color: white;
}

span {
  color: white;
}
</style>
