<template>
  <v-container class="size" fluid grid-list-xl>
    <v-stepper v-model="element" v-touch="{
        left: () => swipe('Left'),
        right: () => swipe('Right'),
        up: () => swipe('Up'),
        down: () => swipe('Down')
      }">

      <v-stepper-header>
        <v-stepper-step :complete="element > 1" step="1">Settings</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="element > 2" step="2">Create</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="element > 3" step="3">Review</v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step :complete="element > 4" step="4">Add Notes</v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1" >
          <OrderSettings />
        </v-stepper-content>
        <v-stepper-content step="2" class="ma-0 pa-0">
          <OrderCreate />
        </v-stepper-content>
        <v-stepper-content step="3" class="ma-0 pa-0">
          <OrderReview />
        </v-stepper-content>
        <v-stepper-content step="4">
          <OrderNotes />
        </v-stepper-content>
        <v-stepper-content step="5">
          <OrderSuccess />

          <div v-if="resp">
            <h3>Status: {{ resp.body.status }}</h3>
          </div>
        </v-stepper-content>
      </v-stepper-items>

      <v-snackbar v-model="snackbarNotifier" :timeout="3000" :color="color">
        <v-icon dark>error</v-icon>
        {{ snackbarText }}
      </v-snackbar>

      <v-footer style="left: 50%; margin-right: -50%; transform: translate(-50%, 0); max-width: 600px"
                fixed height="auto">
        <v-btn v-if="element !== 5" color="primary" flat large @click=goBack>
          <v-icon>arrow_back</v-icon>
          Back
        </v-btn>
        <v-spacer v-if="element !== 5"></v-spacer>
        <v-btn color="primary" v-if="element === 5" block center large @click="this.mainMenu">
              <v-icon>home</v-icon>
              Return to Main Menu
            </v-btn>
        <v-btn color="primary" v-if="element <= 3" flat large @click="this.canProgress" right>
          Next
          <v-icon>arrow_forward</v-icon>
        </v-btn>
        <v-btn color="primary" v-if="element === 4" flat large v-bind:loading="this.isLoading" @click="onSubmitOrder(order, password)">
          Submit Order
        </v-btn>
      </v-footer>
    </v-stepper>
  </v-container>
</template>

<script>
import OrderSettings from './OrderSettings';
import OrderCreate from './OrderCreate';
import OrderReview from './OrderReview';
import OrderNotes from './OrderNotes';
import OrderSuccess from './OrderSuccess';
import store from '../store';
import { apiUrl } from '../data/api'
import { SHOWMAIN, CLEAR_ORDER_SETTINGS, CLEAR_ORDER_ITEMS } from '../store/orders/mutation';

export default {
  name: 'Order',
  store,
  components: {
    OrderSettings,
    OrderCreate,
    OrderReview,
    OrderNotes,
    OrderSuccess,
  },
  computed: {
    order() {
      return this.$store.getters.getOrder;
    },
    password() {
      return this.$store.getters.getPassword;
    },
  },
  data() {
    return {
      element: 1,
      isLoading: false,
      resp: null,
      snackbarNotifier: false,
      color: "error",
      snackbarText: "Please select all settings.",
      returnToHomeDialog: false,
    };
  },
  created: function() {
    this.isOrderContinue()
  },

  methods: {
    isOrderContinue() {
      if (localStorage.getItem('order_items') != null) {
        this.element++
      }
    },
    goBack() {
      if (this.element === 1) {
        this.mainMenu();
        }
      else {
        this.element--;
      }
    },
    mainMenu() {
      this.$store.dispatch(SHOWMAIN);
    },
    canProgress() {
      if (this.$store.getters.getOrderDate != null && this.$store.getters.getDeliveryLocation != null){
        this.element++;
      }
      else {
        this.snackbarText = "Please select all settings.";
        this.snackbarNotifier = true;
      }
    },
    swipe (direction) {
      if (direction === "Right") {
        if (this.element !== 5){
          this.goBack();
        }
      }
      else if (direction === "Left") {
        if (this.element !== 4) {
          this.canProgress();
        }
      }
    },
    onSubmitOrder(order, password) {
      this.isLoading = true;
      order.items = order.items.map(
        category => category.items
          .map(item => ({ ...item, type: category.name }))
      ).reduce(
        (allItems, items) => [...allItems, ...items], []
      );

      const formData = new FormData();
      formData.append('order', JSON.stringify(order));

      const url = `${apiUrl}/place_order?auth_key=${password}`;
      this.$http.post(url, formData)
        .then(
          resp => {
            if (resp.body.status === "order failed") {
              this.snackbarText = "Order Failed";
              this.isLoading = false;
              this.snackbarNotifier = true;
            }
            else {
              this.element = 5;
              this.isLoading = false;
              this.resp = resp;
              this.$store.dispatch(CLEAR_ORDER_ITEMS)
              this.$store.dispatch(CLEAR_ORDER_SETTINGS)
            }
          }
        )
              .catch(err=> {
                this.snackbarText = "No Network Connection";
                this.isLoading = false;
                this.snackbarNotifier = true;
              });
    }
  }
}
</script>

<style>
.size {
  max-width: 100%;
  width: 600px;
}
</style>
