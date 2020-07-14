<template>
  <div class="search">
    <div class="container">
      <h1>Quick Navigation</h1>
    </div><br><br>
    <p>Looking for stock price in certain time period? Click <router-link to="/market">here</router-link>.<br><br>
    </p>
    <p>Review your protfolio performance <router-link to="/portfolio">here</router-link>.<br><br>
    </p>
    <p>Review any particular stock you traded <router-link to="/transaction">here</router-link>.<br><br>
    </p>
  </div>
</template>

<script>
export default {
  name: 'Search',
  data () {
    return {
    }
  },
  methods: {
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}

.container{
  background-color: bisque;
}

img{
  height:150px;
  width:200px;
}

</style>
