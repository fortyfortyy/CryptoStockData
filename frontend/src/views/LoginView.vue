<template>
  <div class="login-container">
    <h1 class="title">Log in</h1>

    <form id="loginPage" class="login-form" @submit.prevent="submitForm">
      <div class="notification-err" v-if="errors.length">
        <p> Couldn't log in. Please try again.</p>
      </div>
      <div class="field">
        <label>Email</label>
        <div class="control">
          <input type="email" placeholder="example@gmail.com" class="input" v-model="email">
        </div>
      </div>

      <div class="field">
        <label>Password</label>
        <div class="control">
          <input type="password" placeholder="********" class="input" v-model="password">
        </div>
      </div>

      <div class="field">
        <div class="control">
          <button class="button">Log in</button>
        </div>
      </div>

      <div>
        <router-link to="/sign-up">click here</router-link>
        to sign up!
      </div>
      <div>
        Or here to
        <router-link to="/password/reset">reset password</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import router from "@/router";

export default {
  name: 'LogIn',
  data() {
    return {
      email: '',
      password: '',
      errors: []
    }
  },
  beforeCreate() {
    this.checkIfAuthenticated()
  },
  mounted() {
    document.title = 'Log In | StockApp'
  },
  methods: {
    async submitForm() {
      if (this.email === '') {
        this.errors.push('Email is missing')
      }
      axios.defaults.headers.common["Authorization"] = ""
      localStorage.removeItem("access")
      localStorage.removeItem("refresh")
      const formData = {
        email: this.email,
        password: this.password,
      }
      await axios
          .post("/api/account/token/", formData)
          .then(response => {
            const access = response.data.access
            const refresh = response.data.refresh
            this.$store.commit('setToken', access, refresh)

            axios.defaults.headers.common["Authorization"] = "Bearer " + access
            localStorage.setItem("access", access)
            localStorage.setItem("refresh", refresh)
            router.push('/stocks')
          })
          .catch(error => {
            if (error.response) {
              for (const property in error.response.data) {
                this.errors.push(`${error.response.data[property]}`)
              }
            } else {
              this.errors.push('Something went wrong. Please try again')

              console.log(JSON.stringify(error))
            }
          })
    },
    checkIfAuthenticated() {
      if (this.$store.state.isAuthenticated) {
        router.push('/stocks')
      }
    }
  }
}
</script>
<style lang="scss">
.login-container {
  display: grid;
  grid-gap: 2rem;
  justify-items: center;
  @media (min-width: 1024px) {
    font-size: 25px !important;
  }

  .title {
    color: #ffffff;
  }
}

.login-container .login-form {
  display: grid;
  grid-gap: 10px;
  justify-items: center;
  min-height: 30vh;
  min-width: 80%;
  @media (min-width: 1024px) {
    grid-gap: 2rem;
  }
}

.login-container .control input {
  padding: 5px;
  border-radius: 5px;
  @media (min-width: 1024px) {
    padding: 10px 40px;
    font-size: 20px;
  }
}

.login-container .notification-err {
  color: mediumvioletred;
}

.button {
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
  background-color: royalblue;
  @media (min-width: 1024px) {
    font-size: 25px !important;
    padding: 15px 60px;
    min-height: 50px;
  }
}

</style>