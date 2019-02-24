<template>
  <div id="app">
    <Airports/>
  </div>
</template>
<script>
import Airports from './components/Airports.vue'
export default {
  name: "Airports",
  components: {
    Airports
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

@import './assets/styles/button.css';
@import './assets/styles/text.css';
</style>
