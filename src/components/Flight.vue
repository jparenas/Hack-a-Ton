<template>
  <div>
    <h1>Liked ones!</h1>
    <div v-for='(val, idx) in info' :key='idx' id='flight'>
      {{ val }}:
      <span>
        <span v-html='val.image'></span> {{ val.image }}
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
  data () {
    return {
      info: null,
      loading: true,
      errored: false,
      current_image_url:'',
    }
  },
  mounted () {
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
  color: black;
}

h1 {
  color: black;
}

span {
  color: black;
}
</style>
