<template>
  <div class="search">
    <router-link to="/">
      <button class="btn btn-primary">Back to homepage</button><br><br>
    </router-link>
    <div class="container">
    <div class="row">
      <div class="col-sm-3 text-center">
        <br><br><img src="../assets/profile.jpg">
      </div>
      <div class="col-sm-8 text-center"><br><br><br>
        <div id="appin">
          <h4>Choose the following three aspects to search</h4><br><br>

        </div>
      </div>
    </div>
    </div><br><br>
    <router-link to="/portfolio">
      <button class="btn btn-secondary">Search Portfolio</button>&nbsp;
    </router-link><br><br>
    <router-link to="/market">
      <button class="btn btn-secondary" >Search Market</button>&nbsp;
    </router-link><br><br>
    <router-link to="/transaction">
      <button class="btn btn-secondary">Search Transaction</button>
    </router-link>
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
