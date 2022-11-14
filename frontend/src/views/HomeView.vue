<template>
  <div class="home">
    <div class="container">
      <h2 class="title">
        Welcome to Crypto Stock!
      </h2>
    </div>

    <div class="crypto-name-container">
      Would you like to check the latest prices of
      <strong id="btc" class="crypto-name">$BTC </strong>
      <strong id="eth" class="crypto-name">$ETH </strong>
      <strong id="bnb" class="crypto-name">$BNB </strong>
      <strong id="sol" class="crypto-name">$SOL </strong>
      <strong id="dome" class="crypto-name">$DOME </strong>

    </div>
    <template v-if="!($store.state.isAuthenticated)">
      <button @click="login()" class="button">Click Here</button>
    </template>

    <template v-else>
      <button @click="prices()" class="button">Click here to see prices</button>
    </template>

  </div>
</template>

<script>

export default {
  name: 'Home',
  mounted() {
    document.title = 'Home | StockApp'
  },
  methods: {
    login() {
      this.$router.push('/login')
    },
    prices() {
      this.$router.push('/stocks')
    }
  }
}
</script>

<style lang="scss">
.home {
  display: grid;
  grid-gap: 3rem;
  justify-items: center;
  color: #ffffff;
  .title {
    font-size: 23px;
    @media (min-width: 1024px) {
      font-size: 37px;
    }
  }

  @media (min-width: 1024px) {
    font-size: 30px !important;
    padding: 10px 40px;
  }

}

.home .crypto-name-container {
  padding: 0 30px;
  text-align: center;
}

.home .crypto-name {
  font-size: 20px !important;
  @media (min-width: 1024px) {
      font-size: 35px !important;
  }

}

.home #btc {
  color: rgba(217, 68, 234);
}

.home #eth {
  color: rgba(200, 68, 234);
}

.home #bnb {
  color: rgb(195, 68, 234);
}

.home #sol {
  color: rgba(200, 68, 234);
}

.home #dome {
  color: rgb(217, 68, 234);
}

.home .button {
  cursor: pointer;
  margin: 10px 0 0;
  font-size: 14px !important;
  height: 40px;
  box-shadow: 0 2px 5px 0 rgba(0, 0, 0, .5);
  align-items: center;
  border: none;
  border-radius: 4px;
  color: #ffffff;
  display: inline-flex;
  flex-direction: row;
  justify-content: center;
  padding: 0 40px;
  position: relative;
  transition: background-color .2s, padding .4s, box-shadow .2s, border .2s;
  background-color: #8144ea !important;

  @media (min-width: 1024px) {
    font-size: 20px !important;
    padding: 10px 40px;
    min-height: 60px;
  }

}

</style>