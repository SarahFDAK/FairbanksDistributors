<template>
    <v-container>
        <h1> Order Settings </h1>
        <v-menu
          v-model="menu"
          :close-on-content-click="true"
          :nudge-right="-10"
          lazy
          transition="scale-transition"
          offset-y
          full-width
          min-width="290px"
        >
          <v-text-field
            slot="activator"
            v-model=orderDate
            label="Delivery Date"
            append-icon="event"
            readonly
          ></v-text-field>
          <v-date-picker v-model="date" v-on:input="menu = onDateChanged(date)"></v-date-picker>
        </v-menu>
        <v-radio-group @change="onStoreNameChanged" v-model="location">
            <template slot="label"> <div class="headline black--text">Delivery Location</div></template>
            <v-divider style="margin-bottom: 10px"></v-divider>

            <template v-for="location in stores">
                <v-radio v-bind:key="location.id" :value="location" color="primary">
                    <template slot="label"> <div class="subheading black--text">{{location.name}}</div></template>
                </v-radio>
            </template>
        </v-radio-group>
    </v-container>
</template>

<script>
import store from '../store';
import { SET_DELIVERY_LOCATION, SET_ORDER_DATE, SET_ORDER_TYPE } from '../store/orders/mutation';

function alaskaTime(){
    var offset = new Date().getTimezoneOffset()/60.0;
    return new Date(new Date().getTime() + 3600000*(-offset));
}

function nextDay(date){
    return new Date(date.getTime() + 86400000);
}

    export default {
        name: "OrderSettings",
        store,
        computed: {
            orderDate() {
                return this.$store.getters.getOrderDate;
            },
            stores() {
                return this.$store.getters.getStores;
            },
            orderTypes() {
                return this.$store.getters.getOrderTypes;
            },
            orderLocation() {
                return this.$store.getters.getDeliveryLocation;
            }
        },
        methods: {
                onDateChanged: function(date) {
                    this.$store.dispatch(SET_ORDER_DATE, date);
                    return false;
                },
                onStoreNameChanged: function(location) {
                    this.$store.dispatch(SET_DELIVERY_LOCATION, location);
                },
                onOrderTypeChanged: function(type) {
                    this.$store.dispatch(SET_ORDER_TYPE, type);
                },
                loadOrderLocation: function () {
                    this.location = this.$store.getters.getDeliveryLocation
                }
        },
        data: () => ({
            routeRep: 'test',
            date: new nextDay(alaskaTime()).toISOString().substr(0, 10),
            menu: false,
            location: null,
        }),
        created: function () {
            this.loadOrderLocation()
        },
    }
</script>

<style>
    /*.v-label {*/
        /*font-size: 32px*/
    /*}*/
</style>
