<template>
  <v-container>
    <h1> Review Order </h1>

    <v-list two-line>
      <template v-for="category in orderItems">
        <v-list v-bind:key="category.name" subheader class="headline">
          <v-icon style="padding-right: 9px; padding-bottom: 7px" small>local_offer</v-icon> {{ category.name}}
        </v-list>
        <template v-for="item in category.items">
          <v-list-tile
            :key="item.name"
            avatar
          >

            <v-list-tile-content>
              <v-list-tile-title>
                {{ item.name.replace(category.name, '') }}
              </v-list-tile-title>
              <v-list-tile-sub-title>
                <b>upc:</b> {{ item.upc }}, <b>oz:</b> {{ item.oz }}, <b>case:</b> {{ item.case }}
              </v-list-tile-sub-title>
            </v-list-tile-content>

          <v-list-tile-action>
             <v-chip color="secondary" text-color="white">
               {{ item.amount }}
             </v-chip>
          </v-list-tile-action>
          </v-list-tile>
        </template>
      </template>

      <v-divider></v-divider>
      <v-spacer></v-spacer>

      <v-list-tile>
        <v-list-tile-content>
          <b>Total Cases:</b>
        </v-list-tile-content>

        <v-list-tile-action>
          <b>{{ totalCases(orderItems) }}</b>
        </v-list-tile-action>
      </v-list-tile>
    </v-list>

  </v-container>
</template>
<script>
import store from '../store';

export default {
  name: 'OrderReview',
  store,
  computed: {
    orderItems() {
      return this.$store.getters.getOrderItems;
    }
  },
  methods:  {
    totalCases: function(orderItems) {
      return orderItems
        .map(category => category.items
          .map(item => item.amount)
          .reduce((a1, a2) => a1 + a2, 0)
        ).reduce((a1, a2) => a1 + a2, 0);
    }
  }
}

</script>

<style>
</style>
