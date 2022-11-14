<template>
  <div class="navbar">
    <template v-if="$store.state.isAuthenticated">
      <router-link to="/stocks" class="stock-item"><strong>Crypto Prices</strong></router-link>
    </template>

    <template v-if="$store.state.isAuthenticated">
      <button id="logout" @click="logout()" class="logout-item">Log out</button>
    </template>

    <template v-else>
      <router-link to="/" class="home-item"><strong>Home</strong></router-link>
      <router-link to="/sign-up" class="sign-up-item"><strong>Sign Up</strong></router-link>
      <router-link to="/login" class="log-in-item">Log in</router-link>
    </template>

  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Navbar",
  methods: {
    logout() {
      axios.defaults.headers.common["Authorization"] = ""
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
      localStorage.removeItem("username")
      this.$store.commit('removeToken')
      this.$router.push('/')
    },
  }
}
</script>

<style lang="scss">
.navbar {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  justify-items: center;
  align-content: center;
  padding: 10px;
  @media (min-width: 1024px) {
    font-size: 25px !important;
    grid-template-columns: repeat(6, 1fr);
  }
}

.home-item {
  grid-column-start: 1 / 2;
}

.stock-item {
  grid-column-end: 2;
  align-self: center;
  @media (min-width: 1024px) {
    font-size: 25px !important;
    //grid-column-start: 1;
  }

}

.logout-item {
  grid-column-start: 4;
    @media (min-width: 1024px) {
    grid-column-start: 6;
  }
}

.sign-up-item {
  grid-column-start: 3;
    @media (min-width: 1024px) {
    grid-column-start: 5;
  }
}

.log-in-item {
  grid-column-start: 3 / 4;
    @media (min-width: 1024px) {
    grid-column-start: 6;
  }
}


#logout {
  text-align: center;
  cursor: pointer;
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
  background-color: royalblue;

  @media (min-width: 1024px) {
    font-size: 25px !important;
    min-height: 5vh;
    padding: 10px 40px;
  }


}
</style>

