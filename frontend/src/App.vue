<script setup>
import {RouterLink, RouterView} from 'vue-router'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'

</script>

<template>
  <Navbar/>

  <div class="main">
    <RouterView/>
  </div>

  <Footer/>
</template>

<script>
import axios from 'axios'
import router from "@/router";

export default {
  mounted() {
    this.verifyToken()
    this.check_and_update_token()
  },
  methods: {
    async refreshToken() {
      if (localStorage.getItem('refresh') && localStorage.getItem('access')) {
        console.log('Refreshing token...')

        let refresh = localStorage.getItem('refresh')
        let access = localStorage.getItem('access')

        axios.defaults.headers.common['Authorization'] = "Bearer " + access

        let data = {
          "refresh": refresh,
        }
        await axios
            .post("/api/account/token/refresh/", data)
            .then(response => {
              if (response.status !== 200) {
                axios.defaults.headers.common["Authorization"] = ""
                this.$store.removeToken()
                const toPath = this.$route.query.to || '/login'
                this.$router.push(toPath)
                this.errors.push('You have to log in again.')
                clearInterval(this.update_timer)
                console.log('Delete timer to update token')
                return
              }

              if (!response.data.access) {
                axios.defaults.headers.common["Authorization"] = ""
                router.push('/login')
                this.errors.push('You have to log in again.')
                clearInterval(this.update_timer)
                console.log('Delete timer for update token')
                return
              }

              const access = response.data.access
              const refresh = response.data.refresh
              console.log('Setting up the new access and refresh tokens')
              axios.defaults.headers.common["Authorization"] = "Bearer " + access
              this.$store.commit('setToken', access, refresh)
              localStorage.setItem("access", access)
              localStorage.setItem("refresh", refresh)
            })
            .catch(error => {
              this.$store.commit('removeToken')
              this.$store.commit('removeTokenFromStorage')
              clearInterval(this.update_timer)
              console.log('Delete timer for update token')
              router.push('/login')
              this.errors.push('You have to log in again.')
              console.log(error)
            })
      } else {
        this.$store.commit('removeToken')
        this.$store.commit('removeTokenFromStorage')

        clearInterval(this.update_timer)
        router.push('/login')
        this.errors.push('You have to log in again.')
      }
    },
    async verifyToken() {
      if (!this.$store.state.access) {
        return
      }
      let data = {
        "refresh": this.$store.state.access,
      }
      await axios
          .post('api/account/token/verify/', data)
          .then(response => {
            if (response.status !== 200) {
              this.refreshToken()
            } else {
              this.$store.state.isAuthenticated = true
            }
          })
          .catch(err => {
            console.log(err)
            this.refreshToken()
          })
    },
    check_and_update_token() {
      this.update_timer = setInterval(() => {
        this.verifyToken()
      }, 24000)
    },
  },

  beforeCreate() {
    this.$store.commit('initializeStore')
    const access = this.$store.state.access
    const refresh = this.$store.state.refresh

    if (access && refresh) {
      axios.defaults.headers.common['Authorization'] = "Bearer " + access
    } else {
      axios.defaults.headers.common['Authorization'] = ""
      clearInterval(this.update_timer)

      if (window.location.pathname.includes('activate')) {
        let path = window.location.pathname.split('/')
        let uidb = path[2]
        let token = path[3]
        const toPath = this.$route.query.to || `/activate/${uidb}/${token}`
        this.$router.push(toPath)
      }

      if (window.location.pathname.includes('/password/set/')) {
        let path = window.location.pathname.split('/')
        let uidb = path[3]
        let token = path[4]
        const toPath = this.$route.query.to || `/password/set/${uidb}/${token}`
        this.$router.push(toPath)
      }
    }
  },

  unmounted() {
    clearInterval(this.update_timer)
  }
}
</script>

<style lang="scss">
.main {
  justify-self: center;
  width: 100%;
  align-self: center;
}
</style>