<template>
  <div>
    <h1>Liked ones!</h1>
    <div v-for='(val, idx) in info' :key='idx' id='flight'>
      {{ val }}:
      <span>
        <span v-html='val.image'></span> {{ val.image }}
      </span>
    </div>
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
      current_image_url: '',
    }
  }
}
</script>

<style>
h1 {
  color: black;
}

span {
  color: black;
}
</style>
