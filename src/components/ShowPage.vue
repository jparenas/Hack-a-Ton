<template>
  <section class='row'>

    <section class='main'>
      <!-- Insert an image -->
      <img id='picture' src='https://img.grouponcdn.com/deal/u2oGrLLtKK5SYv3dVPFZ/GP-2048x1229/v1/c700x420.jpg' width='750'/>

      <!-- Show like and unlike buttons -->
      <div class='controls'>
        <button class="button left"><i class="prev"></i><span class="text-hidden">prev</span></button>
        <button class="button right"><i class="next"></i><span class="text-hidden">next</span></button>
        <!-- <button v-on:click="dislikeHander" class="button left"><i class="prev"></i><span class="text-hidden">prev</span></button>
        <button v-on:click="likeHandler" class="button right"><i class="next"></i><span class="text-hidden">next</span></button> -->
      </div>
    </section>

    <section class='side'>
      <!-- <p>{{count}} times clicked!</p> -->
      <Flight/>
    </section>

  </section>
</template>

<script>
import Flight from'./Flight.vue';

export default {
  name: 'ShowPage',
  props: {
    msg: String
  },
  components: {
    Flight
  }
  // data() {
  //   return {
  //     count: 0
  //   }
  // },
  // methods: {
  //   likeHandler: function(event) {
  //     this.count++,
  //     console.log(this.count)
  //   },
  //   dislikeHander: function(event) {
  //     this.count++,
  //     console.log(this.count)
  //   },
  //   removeElement: function (index) {
  //     this.items.splice(index, 1);
  //   }
  // }
}
</script>

<style scoped>
p {
  color: white;
}
@import '../assets/styles/showpage.css';
@import '../assets/styles/button.css';
</style>
