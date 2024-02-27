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
      <SpreadsheetUpload
        v-else-if="uploadScreenActive"
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
import SpreadsheetUpload from './components/SpreadsheetUpload';
import store from './store';
import { apiUrl } from './data/api';

import {
  LOGIN, LOGOUT, HIDEMAIN,
  SHOWMAIN, SET_CATEGORIES, SET_DATA,
  SHOW_UPLOAD
} from './store/orders/mutation';

export default {
  name: 'App',
  store,
  components: {
    Login,
    MainMenu,
    Order,
    SpreadsheetUpload
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
      const url = `${apiUrl}/items/chips?auth_key=${password}`;
      const freezer_bread_url = `${apiUrl}/items/freezer_bread?auth_key=${password}`;
      
      this.$http.get(url)
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
      this.$store.dispatch(LOGIN, password);
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
      console.log('show upload');
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
