<template>
<div class="top-wrapper">
  <div class="head_title">
    <h2>Trip Matching</h2>
    <!-- <button type="submit" @click.stop.prevent="submit()" class='target_point' id='move_target'>Search</button> -->
    <router-link to='/search'>Let's Search!!</router-link>
    <!-- <a href="#target_point" id="move_target" class="target_point">Let's Serach!!</a> -->
  </div>
</div>
</template>

<script>
export default {
  name: 'Home',
  data () {
    return {

    }
  },
  components: {
  },
  computed: {
    username () {
      // We will see what `params` is shortly
      return ''//this.$route.params.username
    }
  },
  methods: {
    /*
    goBack () {
      window.history.length > 1
        ? this.$router.go(-1)
        : this.$router.push('/')
    }
    */
  }
}
</script>

<style scoped>
@import '../assets/styles/button.css';
</style>
