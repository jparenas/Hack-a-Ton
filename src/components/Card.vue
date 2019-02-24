<template>
  <div class="container card col-md-8">
    <div>
      <img class="destination_image card-body col-md-10" v-bind:src="imageUrl">
    </div>
    <div>
      <h2 class="card-title">{{destination}}</h2>
    </div>
  </div>
</template>

<script>
export default {
  name: "Card",
  props: {
    destination: String,
    imageUrl: String
  },
  data() {
    return {};
  }
};
</script>

<style scoped>
.container {
  background: #f3f3f3;
  border-radius: 15px;
}
</style>