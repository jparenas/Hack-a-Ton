<template>
  <div id='app'>
    <router-view></router-view>
    <!-- <ShowPage msg='Which do you prefer?'/> -->
  </div>
</template>

<script>

export default {
  name: "App",
  components: {
  }
}
</script>

<style scoped>
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
