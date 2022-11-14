<template>
  <div class="stock-container">
    <div class="box">
      <p class="" v-for="(value) in stock ">
        {{ name }} - ${{ value }}
      </p>

    </div>
  </div>
</template>

<script>
export default {
  name: "StockPrice",
  props: {
    stock: Object,
    name: toString()
  }
}
</script>

<style scoped>
.stock-container {
  padding: 5px;
}
</style>