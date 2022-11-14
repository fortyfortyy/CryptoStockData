<template>
  <footer class="footer" id="footer">
    <p class="has-text-centered">Copyright (C) 2022 Daniel Pacek</p>
  </footer>
</template>

<script>
export default {
  name: "Footer"
}
</script>

<style lang="scss">
.footer {
  font-size: 13px;
  align-self: center;
  padding: 10px;
  border-radius: 4px;
  color: #ffffff;
  margin-top: 30px;
  background-color: royalblue;
  @media (min-width: 1024px) {
    font-size: 18px !important;
    font-family: "Roboto", "Lucida Grande", "DejaVu Sans", "Bitstream Vera Sans", Verdana, Arial, sans-serif;;
  }

}

.footer p {
  text-align: center;
}
</style>