<template>
  <v-container fill-height class="size">
    <v-dialog v-model="createNewOrderDialog">
        <v-card>
          <v-card-title class="headline">Discard Order?</v-card-title>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="primary" flat
              @click="createNewOrderDialog = false"
            >
              No
            </v-btn>

            <v-btn
              color="primary" flat
              @click="newOrder(tempType)"
            >
              Yes
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-container>
          <v-layout
          align-space-around
          text-xs-center
          pa-5
          column>
              <template v-for="type of orderTypes">
                <v-flex v-if="type === 'Chips' || type === 'Freezer Bread'">
                  <v-btn round block large color="primary"
                          @click="onOrderTypeSelected(type)">{{type}} Order
                  </v-btn>
                </v-flex>

                <v-flex v-else>
                  <v-btn round block large disabled color="primary"
                          @click="onOrderTypeSelected(type)">{{type}} Order
                  </v-btn>
                </v-flex>
              </template>

              <v-divider style="margin: 10px 0"></v-divider>

              <v-flex>
                <v-btn round block large
                  :disabled="isContinueOrderDisabled"
                  v-on:click=onOrderContinue
                  color=info>
                   Continue Order
                </v-btn>
              </v-flex>
              <!-- <v-flex>
                <v-btn round block large disabled

                  v-on:click=spreadsheetUpload
                  color=info>
                   Update Order Items
                </v-btn>
              </v-flex> -->
              <v-flex>
                <v-btn round block large disabled
                  color=info>
                    Settings
                </v-btn>
              </v-flex>
              <v-flex>
                <v-btn round block large dark
                  color=secondary
                  v-on:click="$emit('Logout')">
                    Logout
                </v-btn>
              </v-flex>
          </v-layout>
      </v-container>
  </v-container>
</template>

<script>
import store from '../store';
import { CLEAR_ORDER_ITEMS, CLEAR_ORDER_SETTINGS, SET_ORDER_TYPE, SET_DATA, LOAD_ITEM_DATA, RESTORE_ORDER } from "../store/orders/mutation";

export default {
  name: 'MainMenu',
  store,
  data () {
    return {
      createNewOrderDialog: false,
      tempType: null
    };
  },
  computed: {
    orderTypes() {
        return this.$store.getters.getOrderTypes;
    },
    isContinueOrderDisabled() {
      return localStorage.getItem('order_items') == null;
    },
  },
  methods:    {
    newOrder: function (type) {
      var item_type;
      if (type === 'Chips') {
        item_type = 'chips';
        this.$store.dispatch(SET_ORDER_TYPE, type);
      }
      else if (type === 'Freezer Bread') {
        item_type = 'freezer_bread';
        this.$store.dispatch(SET_ORDER_TYPE, item_type);
      }
      localStorage.setItem('order_type', item_type)
      this.$store.dispatch(LOAD_ITEM_DATA, item_type);
      this.$store.dispatch(CLEAR_ORDER_ITEMS);
      this.$store.dispatch(CLEAR_ORDER_SETTINGS);
      this.$emit('createOrder');
    },
    spreadsheetUpload: function() {
      this.$emit('spreadsheetUpload');
    },
    onOrderTypeSelected: function(type) {
      if (localStorage.getItem('order_items') != null) {
        this.tempType = type;
        this.createNewOrderDialog = true;
      }
      else {
        this.newOrder(type)
      }
    },
    onOrderContinue: function() {
      this.$store.dispatch(LOAD_ITEM_DATA, localStorage.getItem('order_type'));
      this.$store.dispatch(RESTORE_ORDER);
      this.$emit('createOrder');
    },
  }
}
</script>

<style>
.size {
  max-width: 100%;
  width: 600px;
}
</style>
