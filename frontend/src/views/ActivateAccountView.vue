<template>
  <div class="forgot-main-container">
    <div class="forgot-container">
      <h1 class="title">Activate your account</h1>
      <h4>Please click the button below to activate your account.</h4>

      <div class="notification-success" v-if="success.length">
        <p v-for="sucess in success" v-bind:key="sucess">{{ sucess }} </p>
        <router-link to="/login" class="link-log-in"><strong>Click here to log in</strong></router-link>
      </div>

      <form id="loginPage" class="forgot-form" @submit.prevent="submitForm">
        <div class="notification-err" v-if="errors.length">
          <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
        </div>
        <div class="field">
          <div class="control">
            <button class="button">Activate</button>
          </div>
        </div>

      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ActivateAccount',
  data() {
    return {
      token: "",
      uidb: "",
      errors: [],
      success: [],
    }
  },
  mounted() {
    document.title = 'Activate Account | StockApp'
  },
  methods: {
    async submitForm() {
      const bodyData = {
        "uidb64": this.uidb,
        "token": this.token,
      }
      this.extractTokensFromUrl()
      axios.defaults.headers.common["Authorization"] = ""

      await axios
          .patch(`/api/account/activate/${this.uidb}/${this.token}/`, bodyData)
          .then(response => {
            if (response.status !== 200) {
              this.errors.push(response.data.detail)
              console.log(JSON.stringify(response))
            } else {
              this.success.push('Account has been activated!')
            }
          })
          .catch(error => {
            if (error.response) {
              for (const property in error.response.data) {
                this.errors.push(`${error.response.data[property]}`)
              }
            } else {
              console.log(JSON.stringify(error))
            }
          })
    },
    extractTokensFromUrl() {
      const currentURL = window.location.pathname.split('/')
      this.token = currentURL[3]
      this.uidb = currentURL[2]
    },
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