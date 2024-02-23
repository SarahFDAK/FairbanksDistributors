export const LOGIN = 'login';
export const LOGOUT = 'logout';
export const SHOWMAIN = 'showMain';
export const HIDEMAIN = 'hideMain';
export const SHOW_UPLOAD = 'showUpload';
export const HIDE_UPLOAD = 'hideUpload';

export const SET_STORES = 'setStores';
export const SET_SELECTED_ITEM_TYPE = 'setSelectedItemType';
export const SET_CATEGORIES = 'setCategories';
export const SET_DATA = 'setData';

export const LOAD_ITEM_DATA = 'loadItemData';
export const RESTORE_ORDER = 'restoreOrder';

export const ADD_ORDER_ITEM = 'addOrderItem';
export const CLEAR_ORDER_ITEMS = 'clearOrderItems';
export const CLEAR_ORDER_SETTINGS = 'clearOrderSettings';

export const SUBMIT_ORDER = 'submitOrder';

export const SET_DELIVERY_LOCATION = 'setDeliveryLocation';
export const SET_ORDER_DATE = 'setOrderDate';
export const SET_ORDER_TYPE = 'setOrderType';

export const ADD_ORDER_NOTES = 'addOrderNotes';

export const mutations = {
  [LOGIN]: function(state, password) {
    state.isLoggedIn = true;
    state.mainMenu = true;
    state.password = password;
    localStorage.setItem("password", password);
  },

  [LOGOUT]: function(state) {
    state.isLoggedIn = false;
    state.mainMenu = false;
    state.password = null;
  },

  [SET_CATEGORIES]: function(state, categories) {
    state.categories = categories;
    state.itemTypes = categories.map(category => category.name);
  },

  [SET_DATA]: function(state, data_tuple) {
    state.order_data_tuples[data_tuple.data_type] = data_tuple.data;
  },

  [SET_STORES]: function(state, stores) {
    state.stores = stores;
  },

  [LOAD_ITEM_DATA]: function(state, type) {
    const { categories } = state.order_data_tuples[type];
    let categoriesWithAmount = [];

    for (const category of categories) {
      const { items, name } = category;

      const withAmount = items
        .map(item => ({...item, amount: 0}));

      categoriesWithAmount = [...categoriesWithAmount, { name, items: withAmount }];
    }
    state.categories = categoriesWithAmount;
    state.itemTypes = categoriesWithAmount.map(category => category.name);
  },

  [SHOWMAIN]: function(state) {
    state.mainMenu = true;
  },

  [HIDEMAIN]: function(state) {
    state.mainMenu = false;
  },

  [SHOW_UPLOAD]: function(state) {
    state.orderUpdateScreen = true;
  },

  [HIDE_UPLOAD]: function(state) {
    state.orderUpdateScreen = false;
  },

  [ADD_ORDER_ITEM]: function(state, orderItem) {
    state.categories
      .map(category => category.items
        .filter(item => item === orderItem.item)
        .forEach(item => item.amount = orderItem.amount)
      )
    localStorage.setItem('order_items', JSON.stringify(state.categories))
  },

  [RESTORE_ORDER]: function(state) {
    if (localStorage.getItem('order_items') != null) {
      state.categories = JSON.parse(localStorage.getItem('order_items'));
    }
    if (localStorage.getItem('order_notes') != null) {
      state.order.orderNotes = localStorage.getItem('order_notes')
    }
    state.order.deliveryLocation = JSON.parse(
      localStorage.getItem('order_location')
    );
  },

  [SET_SELECTED_ITEM_TYPE]: function(state, type) {
    state.selectedType = type;
  },

  [CLEAR_ORDER_ITEMS]: function(state) {
    state.categories = state.categories.map(category => ({
        ...category,
        items: category.items.map(item => {
          item.amount = 0;
          return item;
        })
      })
    );
    state.selectedType = null;
    localStorage.removeItem('order_items')
  },

  [CLEAR_ORDER_SETTINGS]: function(state) {
    state.order.deliveryLocation = null;
    state.order.orderNotes = '';
    localStorage.removeItem('order_notes')
    localStorage.removeItem('order_location')
  },

  [SUBMIT_ORDER]: function(state) {
    state.submit = true;
  },

  [SET_DELIVERY_LOCATION]: function(state, store) {
    state.order.deliveryLocation = store;
    localStorage.setItem('order_location', JSON.stringify(store));
  },

  [SET_ORDER_DATE]: function(state, date) {
    state.order.date = date;
  },

  [SET_ORDER_TYPE]: function(state, type) {
    state.order.type = type;
  },

  [ADD_ORDER_NOTES]: function(state, notes) {
    state.order.orderNotes = notes;
    localStorage.setItem('order_notes', notes)
  }
};
