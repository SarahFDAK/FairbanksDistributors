import {
  LOGIN,
  LOGOUT,
  ADD_ORDER_ITEM,
  CLEAR_ORDER_ITEMS,
  CLEAR_ORDER_SETTINGS,
  SUBMIT_ORDER,
  SET_SELECTED_ITEM_TYPE,
  SET_ORDER_DATE,
  SET_DELIVERY_LOCATION,
  SET_CATEGORIES,
  SET_DATA,
  SET_STORES,
  LOAD_ITEM_DATA,
  HIDEMAIN,
  SHOWMAIN,
  SHOW_UPLOAD,
  HIDE_UPLOAD,
  ADD_ORDER_NOTES,
  SET_ORDER_TYPE,
  RESTORE_ORDER,
} from './mutation';

export default {
  login({ commit }, password) {
    commit(LOGIN, password);
  },

  logout({ commit }) {
    commit(LOGOUT);
  },

  hideMain({ commit }) {
    commit(HIDEMAIN);
  },

  showUpload({ commit }) {
    commit(SHOW_UPLOAD);
  },

  hideUpload({ commit }) {
    commit(HIDE_UPLOAD);
  },

  setCategories({ commit }, categories) {
    commit(SET_CATEGORIES, categories);
  },

  setStores({ commit }, stores) {
    commit(SET_STORES, stores);
  },

  setData({ commit }, data_tuple) {
    commit(SET_DATA, data_tuple);
  },

  loadItemData({ commit}, data_type) {
    commit(LOAD_ITEM_DATA, data_type);
  },

  restoreOrder({ commit }) {
    commit(RESTORE_ORDER);
  },

  showMain({ commit }) {
    commit(SHOWMAIN);
  },

  addOrderItem({ commit }, item) {
    commit(ADD_ORDER_ITEM, item);
  },

  setSelectedItemType({ commit }, type) {
    commit(SET_SELECTED_ITEM_TYPE, type);
  },

  clearOrderItems({ commit }) {
    commit(CLEAR_ORDER_ITEMS);
  },

  clearOrderSettings({ commit }) {
    commit(CLEAR_ORDER_SETTINGS);
  },

  submitOrder({ commit }) {
    commit(SUBMIT_ORDER);
  },

  setOrderDate({ commit }, date) {
    commit(SET_ORDER_DATE, date);
  },

  setOrderType({ commit }, type) {
    commit(SET_ORDER_TYPE, type);
  },

  setDeliveryLocation({ commit}, location) {
    commit(SET_DELIVERY_LOCATION, location);
  },

  addOrderNotes({ commit }, notes) {
    commit(ADD_ORDER_NOTES, notes);
  }

};
