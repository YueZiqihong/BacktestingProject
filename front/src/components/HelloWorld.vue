<template>
<div class="hello">
  <h1>{{ msg }}</h1>
  <h2>Essential Links</h2>
  <ul>
    <li>
      <a href="https://www.google.com" target="_blank">
        谷歌
      </a>
    </li>
    <li>
      <router-link to="/backtesting">
        <button class="btn btn-default">Start testing</button>
      </router-link>
    </li>
  </ul>
  <h2>Test</h2>



  <el-input v-model="testA" placeholder="a" style="display:inline-table; width: 30%; float:left"></el-input>
  <el-input v-model="testB" placeholder="b" style="display:inline-table; width: 30%; float:left"></el-input>
  <el-button type="primary" @click="test(testA,testB)" style="float:left; margin: 2px;">test</el-button>
  <p>{{testout}}</p>
  <el-button type="primary" @click="backtest" style="float:left; margin: 2px;">backtest</el-button>

</div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      msg: 'Welcome to Your Vue.js App',
      testA: 0,
      testB: 0,
      testout: 0,
    }
  },
  methods: {
    test: function(a,b) {
      this.axios.get('http://127.0.0.1:8000/api/test', {
        params: {
        a: a,
        b: b
        }
      })
      .then((response) => {
        this.testout = response.data.testdata
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    backtest: function() {
      this.axios.get('http://127.0.0.1:8000/api/backtest')
      .then((response) => {
        alert("done")
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      })
    }


  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
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

a {
  color: #42b983;
}
</style>
