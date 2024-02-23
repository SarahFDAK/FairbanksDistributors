<template>
  <v-app v-show="checkedStorage">
    <v-toolbar app v-if="isLoggedIn">
      <v-toolbar-items>
        <v-btn large icon v-on:click="goHome">
          <v-img :src="require('./assets/FD_Monogram.png')" contain></v-img>
        </v-btn>
      </v-toolbar-items>
      <v-toolbar-title class="headline text-uppercase">
        <span>FD</span>
        <span class="font-weight-light ml-2" >ORDER APP</span>
      </v-toolbar-title>

      <v-spacer></v-spacer>

    </v-toolbar>

    <v-content>
      <Login
        v-if="!isLoggedIn"
        v-on:login="onLoggin($event)"
      />
      <MainMenu
        v-else-if="mainMenuActive"
        v-on:createOrder="createOrder"
        v-on:Logout="onLogout"
        v-on:spreadsheetUpload="setUploadSpreadsheetMenu"
      />
      <!--add new screen for order confirmation here-->
      <Order v-else/>
    </v-content>
  </v-app>
</template>

<script>
import Login from './components/Login';
import Order from './components/Order';
import MainMenu from './components/MainMenu';
import store from './store';
import { apiUrl } from './data/api';

import {
  LOGIN, LOGOUT, HIDEMAIN,
  SHOWMAIN, SET_DATA,
  SHOW_UPLOAD, SET_STORES
} from './store/orders/mutation';

export default {
  name: 'App',
  store,
  components: {
    Login,
    MainMenu,
    Order,
  },
  data: () => ({
    checkedStorage: false,
  }),
  methods: {
    checkStorage: function() {
      if (localStorage.getItem("password")) {
          this.onLoggin(localStorage.getItem("password"));
        }
      else {
        this.checkedStorage = true;
      }
    },
    onLoggin: function(password) {
      const chips_url = `${apiUrl}/chips/items?auth_key=${password}`;
      const freezer_bread_url = `${apiUrl}/freezer_bread/items?auth_key=${password}`;

      this.$http.get(chips_url)
        .then(resp => {
          this.checkedStorage = true;
          const chip_tuple = {data_type: 'chips', data: resp.body};
          this.$store.dispatch(SET_DATA, chip_tuple);
        })

      this.$http.get(freezer_bread_url)
        .then(resp => {
          const freezer_bread_tuple = {data_type: 'freezer_bread', data: resp.body};
          this.$store.dispatch(SET_DATA, freezer_bread_tuple);
        })

      this.loadStores(password);

      this.$store.dispatch(LOGIN, password);
    },
    loadStores: function(password) {
      const storesUrl = `${apiUrl}/stores?auth_key=${password}`;

      this.$http.get(storesUrl).then(
        resp => {
          const stores = resp.body;
          this.$store.dispatch(SET_STORES, stores);
        }
      );
    },
    onLogout: function() {
      this.$store.dispatch(LOGOUT);
      localStorage.removeItem("password");
    },
    createOrder: function() {
      this.$store.dispatch(HIDEMAIN);
    },
    goHome: function() {
      this.$store.dispatch(SHOWMAIN);
    },
    setUploadSpreadsheetMenu: function() {
      this.$store.dispatch(SHOW_UPLOAD);
    }
  },
  computed: {
    isLoggedIn() {
      this.checkStorage();
      return this.$store.getters.getIsLoggedIn;
    },
    mainMenuActive() {
      return this.$store.getters.getIsMainMenuActive;
    },
    uploadScreenActive() {
      return this.$store.getters.getIsOrderUpdateActive;
    }
  }
}
</script>

<style>
</style>
