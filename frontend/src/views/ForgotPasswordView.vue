<template>
  <div class="forgot-main-container">
    <div class="forgot-container">
      <h1 class="title">Forgotten your password?</h1>
      <h4>Enter your email address to reset your password. You may need to check your spam folder.</h4>

      <div class="notification-success" v-if="success.length">
        <p v-for="sucess in success" v-bind:key="sucess">{{ sucess }} </p>
      </div>

      <form class="forgot-form" @submit.prevent="submitForm">

        <div class="notification-err" v-if="errors.length">
          <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
        </div>
        <div class="field">
          <label>Email</label>
          <div class="control">
            <input type="email" placeholder="example@gmail.com" class="input" v-model="email">
          </div>
        </div>

        <div class="field">
          <div class="control">
            <button class="button">Submit</button>
          </div>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ForgotPassword',
  data() {
    return {
      email: '',
      errors: [],
      success: [],
    }
  },
  mounted() {
    document.title = 'Forgot Password | StockApp'
  },
  methods: {
    async submitForm() {
      const formData = {
        email: this.email,
      }

      axios.defaults.headers.common["Authorization"] = ""
      await axios
          .post("/api/account/password/reset/", formData)
          .then(response => {
            if (response.status !== 200) {
              console.log(JSON.stringify(response))
            } else {
              this.success.push(response.data.detail)
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
    }
  }
}
</script>
<style lang="scss">
.forgot-main-container {
  display: grid;
  justify-items: center;

  @media (min-width: 1024px) {
    font-size: 25px !important;
  }

  .title {
    color: #ffffff;
  }
}

.forgot-container .forgot-form {
  margin-top: 30px;
  display: grid;
  grid-gap: 1rem;

  @media (min-width: 1024px) {
    grid-gap: 2rem;
  }
}

.forgot-container .control input {
  padding: 5px;
  border-radius: 5px;
  @media (min-width: 1024px) {
    padding: 10px 40px;
    font-size: 20px;
  }
}

.forgot-container .notification-err {
  color: mediumvioletred;
}


.forgot-container .notification-success{
  color: darkgreen;
}


.forgot-container .button {
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