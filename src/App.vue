<template>
  <div id='app'>
    <ShowPage msg='Which do you prefer?'/>
  </div>
</template>

<script>
import ShowPage from './components/ShowPage.vue'

export default {
  name: "Airports",
  components: {
    ShowPage
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
