<template>
  <div class="stock-container">
    <div class="box">
      <div class="" v-for="(value, index) in stock" :key="value">
        {{ index }} - ${{ value }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "StockPrice",
  props: {
    stock: Object,
    // key: toString()
  }
}
</script>

<style scoped>
.stock-container {
  padding: 5px;
}
</style>