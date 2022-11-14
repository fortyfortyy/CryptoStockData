<template>
  <div class="register-container">


    <h1 class="title">Sign up</h1>

    <div class="notification-err" v-if="errors.length">
      <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
    </div>

    <form class="register-form" @submit.prevent="submitForm">
      <div class="field">
        <label>Username</label>
        <div class="control">
          <input type="text" placeholder="JhonyBravo" class="input" v-model="username">
        </div>
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
        <label>Repeat password</label>
        <div class="control">
          <input type="password" placeholder="********" class="input" v-model="password2">
        </div>
      </div>

      <div class="field">
        <div class="control">
          <button class="button is-dark">Sign up</button>
        </div>
      </div>
      <div>
        Or here to
        <router-link to="/login">log in</router-link>
      </div>
    </form>
  </div>

</template>

<script>
import axios from 'axios'
import router from "@/router";

export default {
  name: 'SignUp',
  data() {
    return {
      email: '',
      password: '',
      password2: '',
      username: '',
      errors: []
    }
  },
  beforeCreate() {
    this.checkIfAuthenticated()
  },
  mounted() {
    document.title = 'Register | StockApp'
  },
  methods: {
    submitForm() {
      this.errors = []
      if (this.email === '') {
        this.errors.push('The email is missing')
      }
      if (this.username === '') {
        this.errors.push('The username is missing')
      }
      if (this.password === '') {
        this.errors.push('The password is too short')
      }
      if (this.password !== this.password2) {
        this.errors.push('The passwords doesn\'t match')
      }
      if (!this.errors.length) {
        const formData = {
          username: this.username,
          email: this.email,
          password: this.password,
          password2: this.password2,
        }
        axios.defaults.headers.common["Authorization"] = ""
        axios
            .post("/api/account/register/", formData)
            .then(response => {
              if (response.status === 201) {
                this.errors.push('Please check your email to activate account.')
              } else {
                this.errors.push('Something gone wrong...')
              }
              setTimeout(() => router.push('/login'), 5000)

            })
            .catch(error => {
              if (error.response) {
                for (const property in error.response.data) {
                  this.errors.push(`${property}: ${error.response.data[property]}`)
                }
                console.log(JSON.stringify(error.response.data))
              } else if (error.message) {
                this.errors.push('Something went wrong. Please try again')

                console.log(JSON.stringify(error))
              }
            })
      }
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
.register-container {
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

.register-container .register-form {
  display: grid;
  grid-gap: 5px;
  justify-items: center;
  min-height: 30vh;
  min-width: 80%;
  @media (min-width: 1024px) {
    grid-gap: 2rem;
  }

  .field {
    padding: 3px;
  }
}

.register-container .control input {
  padding: 5px;
  border-radius: 5px;
  @media (min-width: 1024px) {
    padding: 10px 40px;
    font-size: 20px;
  }

}

.register-container .notification-err {
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
    padding: 10px 60px;
    min-height: 50px;
  }

}

</style>