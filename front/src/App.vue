<template>
  <div id="app">
    <div id="logo">
      <h1><img src="./assets/web.png" float="left"> Welcome to our backtestingsystem!</h1>
    </div>

    <el-menu :default-active="this.$router.path" mode="horizontal" router
    @select="handleSelect">
      <el-menu-item index="/">Homepage</el-menu-item>
      <el-menu-item index="/upload">Upload</el-menu-item>

      <el-submenu index="Backtesting">
      <template slot="title">Backtesting</template>
      <el-menu-item index="/pool">Setting Stock Pool</el-menu-item>
      <el-menu-item index="/backtesting">Setting Strategy and Time</el-menu-item>
      </el-submenu>

      <el-submenu index="Graphs">
      <template slot="title">See graphs</template>
      <el-menu-item index="/market">Review Market Data</el-menu-item>
      <el-menu-item index="/portfolio">See Portfolio Performance</el-menu-item>
      <el-menu-item index="/transaction">Review Historical Transactions</el-menu-item>
      </el-submenu>

      <el-menu-item index="" disabled>Coming soon</el-menu-item>
    </el-menu>

    <router-view/>
  </div>
</template>

<script>

export default {
  data() {
    return {
      name: 'App',
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    }
  }
}

</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
