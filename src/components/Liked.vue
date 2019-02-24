<template>
    <div>
        <h3 v-if='liked'>{{destination}} - {{price}} <span v-if="super_liked">⭐</span></h3>
    </div>
</template>

<script>
export default {
    name: "Liked",
    props: {
        destination: String,
        price: String,
        super_liked: Boolean,
        liked: Boolean
    },
    data() {
        return {};
    }
}
</script>

<style scoped>

</style>
