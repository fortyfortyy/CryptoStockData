<template>
  <div class="stock-prices-container">
    <h1 class="title">Current Prices</h1>
    <div class="stock-data">
      <StockPrice
          v-for="(stock) in latestCryptoPrices"
          v-bind:key="stock"
          v-bind:stock="stock"
      />
    </div>

  </div>
</template>

<script>
import axios from 'axios'
import StockPrice from '@/components/StockPrice.vue'
import router from "@/router";

export default {
  name: 'StockPrices',
  data() {
    return {
      latestCryptoPrices: []
    }
  },
  components: {
    StockPrice
  },
  mounted() {
    this.getLatestCryptoPrices()
    document.title = 'Crypto Prices | StockApp'

    this.price_update_timer = setInterval(() => {
      console.log('Set timer to recieve stock data every 5 sec')
      this.getLatestCryptoPrices()
    }, 5000)
  },

  methods: {
    async getLatestCryptoPrices() {
      if (!this.$store.state.isAuthenticated) {
        clearInterval(this.timer)
        router.push('/')
        return
      }

      console.log('Updating crypto prices...')
      await axios
          .get('/api/stocks/')
          .then(response => {
            if (response.status !== 200){
              this.$store.refreshToken()
            }
            this.latestCryptoPrices = response.data
          })
          .catch(error => {
            console.log(error)
            this.verifyToken()
          })
    },
  },

  unmounted() {
    console.log('niszcze price_update_timer')
    clearInterval(this.price_update_timer)
  }
}
</script>


<style lang="scss">
.stock-prices-container {
  color: #ffffff;
  display: grid;
  grid-gap: 2rem;
  grid-template-rows: 0.5fr 2fr;
  justify-content: center;
  align-content: center;

  @media (min-width: 1024px) {
    margin-top: 30px;
    font-size: 30px !important;
  }

}

.stock-prices-container .title {
  background: -webkit-linear-gradient(rgb(224, 23, 221), rgba(10, 115, 231, 0.89));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

</style>