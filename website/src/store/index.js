import actions from './orders/actions';
import { mutations } from './orders/mutation';
import { getters } from './orders/getters';
import { storeNames } from './routes';
import Vuex from 'vuex';

function alaskaTime(){
    var offset = new Date().getTimezoneOffset()/60.0;
    return new Date(new Date().getTime() + 3600000*(-offset));
}

function nextDay(date){
    return new Date(date.getTime() + 86400000);
}

export default new Vuex.Store({
  strict: true,
  state: {
    password: null,
    isLoggedIn: false,
    mainMenu: false,
    orderUpdateScreen: false,
    categories: [],
    itemTypes: [],
    selectedType: null,
    order: {
      items:[],
      date: new nextDay(alaskaTime()).toISOString().substr(0, 10),
      deliveryLocation: null,
      type: 'Chips',
      orderNotes: '',
    },
    storeNames: storeNames,
    orderTypes: ['Chips', 'Frozen Bread', 'Fresh Bread', 'Tortillas/Salsa'],
  },
  actions,
  mutations,
  getters,
});
