const getOrderItems =
  state => state.categories.map(
    category => ({
      ...category,
      items: category.items
        .filter(item => item.amount !== 0)
    }))
    .filter(category => category.items.length !== 0)


export const getters = {
  getPassword: state => state.password,
  getIsLoggedIn: state => state.isLoggedIn,
  getIsMainMenuActive: state => state.mainMenu,
  getIsOrderUpdateActive: state => state.orderUpdateScreen,
  getCategories: state => state.categories,
  getItemTypes: state => state.itemTypes,
  getSelectedType: state => state.selectedType,
  getSelectedItems: state => state.categories
    .map(category => category.items
    .filter(item => item.type === state.selectedType)),
  getOrderItems,
  getRouteRep: state => state.routeRep,
  getOrderDate: state => state.order.date,
  getOrderType: state => state.order.type,
  getStoreNames: state => state.storeNames,
  getOrderTypes: state => state.orderTypes,
  getDeliveryLocation: state => state.order.deliveryLocation,
  getOrderNotes: state => state.order.orderNotes,
  getOrder: state => ({
    store: state.order.deliveryLocation,
    items: getOrderItems(state),
    date: state.order.date,
    notes: state.order.orderNotes,
  })
};
