<template>
  <div class="password-set-container">
    <h1 class="title">Set new password</h1>

    <div class="notification-success" v-if="success.length">
      <p v-for="sucess in success" v-bind:key="sucess">{{ sucess }} </p>
      <router-link to="/login" class="link-log-in"><strong>Click here to log in</strong></router-link>
    </div>

    <form id="passwordSet" class="password-set-form" @submit.prevent="submitForm">
      <div class="notification-err" v-if="errors.length">
        <p> Couldn't set new password.</p>
      </div>
      <div class="field">
        <label>First Password</label>
        <div class="control">
          <input type="password" placeholder="********" class="input" v-model="password">
        </div>
      </div>

      <div class="field">
        <label>Repeat Password</label>
        <div class="control">
          <input type="password" placeholder="********" class="input" v-model="password2">
        </div>
      </div>

      <div class="field">
        <div class="control">
          <button class="button">Submit</button>
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import router from "@/router";

export default {
  name: 'PasswordSet',
  data() {
    return {
      uidb: '',
      token: '',
      password: '',
      password2: '',
      errors: [],
      success: [],
    }
  },
  mounted() {
    this.checkIfAuthenticated()
    document.title = 'Set new password | StockApp'
  },
  methods: {
    async submitForm() {
      if (this.password === '' || this.password2 === '') {
        this.errors.push('Password field is missing')
      }
      if (this.password !== this.password2) {
        this.errors.push('Passwords are not the same')
      }
      if (this.password.length < 9 || this.password2.length < 9) {
        this.errors.push('Password has to have more than 8 characters')
      }

      const formData = {
        password: this.password,
        password2: this.password2,
      }

      this.extractTokensFromUrl()
      axios.defaults.headers.common["Authorization"] = ""

      await axios
          .put(`/api/account/password/set/${this.uidb}/${this.token}/`, formData)
          .then(response => {
            if (response.status === 200) {
              this.success.push(`You have successfully set the new password`)
              router.push('/login')
            }
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
    extractTokensFromUrl() {
      const currentURL = window.location.pathname.split('/')
      console.log(currentURL)
      this.uidb = currentURL[3]
      this.token = currentURL[4]
    },
    checkIfAuthenticated() {
      if (this.$store.state.isAuthenticated) {
        router.push('/stocks')
      }
    },
  }
}
</script>

<style lang="scss">
.password-set-container {
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

.password-set-container .password-set-form {
  display: grid;
  grid-gap: 10px;
  justify-items: center;
  min-height: 30vh;
  min-width: 80%;
  @media (min-width: 1024px) {
    grid-gap: 2rem;
  }
}

.password-set-container .control input {
  padding: 5px;
  border-radius: 5px;
  @media (min-width: 1024px) {
    padding: 10px 40px;
    font-size: 20px;
  }
}

.password-set-container .notification-err {
  color: mediumvioletred;
}

.password-set-container .notification-success {
  color: darkgreen;
  text-align: center;
}

.password-set-container .button {
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