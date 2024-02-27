<template>
  <v-container>
    <h1> Order Submitted </h1>
    <h2> Delivery Location: {{ deliveryLocation }}</h2>
    <h2> Delivery date: {{ orderDate }} </h2>
  </v-container>
</template>
<script>
import store from '../store';

export default {
  name: 'Success',
  store,
        computed: {
            orderDate() {
                return this.$store.getters.getOrderDate;
            },
            deliveryLocation() {
                return this.$store.getters.getDeliveryLocation;
            }
        },
}

</script>

<style>
</style>
