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
    <li>
      <router-link to="/upload">
        <button class="btn btn-default">Upload csv</button>
      </router-link>
    </li>
  </ul>
  <h2>Test</h2>



  <el-input v-model="testA" placeholder="a" style="display:inline-table; width: 30%; float:left"></el-input>
  <el-input v-model="testB" placeholder="b" style="display:inline-table; width: 30%; float:left"></el-input>
  <el-button type="primary" @click="test(testA,testB)" style="float:left; margin: 2px;">test</el-button>
  <p>{{testout}}</p>
  <el-button @click="test2(testA, testB)" style="float:left; margin: 2px;">test2</el-button>

  <el-button type="primary" @click="getPortfolio(testA,testB)" style="float:left; margin: 2px;">Portfolio</el-button>
  <br><br>
  <el-button type="primary" @click="getMarket(testA,testB)" style="float:left; margin: 2px;">Market</el-button>
  <el-button type="primary" @click="getTransaction(testA,testB)" style="float:left; margin: 2px;">Transaction</el-button>
  <el-button type="primary" @click="getBookList" style="float:left; margin: 2px;">Getlist</el-button>
  <br><br><br>

  <div id="testChart1" style="width: 600px;height:400px;"></div>
  <br><br><br>
  <div id="testChart2" style="width: 600px;height:400px;"></div>
  <br><br><br>
  <div id="testChart3" style="width: 600px;height:400px;"></div>
  <br><br><br>
  <div id="testChart4" style="width: 600px;height:400px;"></div>
  <br><br><br>
  <div id="testChart5" style="width: 600px;height:400px;"></div>

</div>

</template>

<script>
import echarts from 'echarts'

export default {
  name: 'HelloWorld',
  data() {
    return {
      msg: 'Welcome to Your Vue.js App',
      testA: 0,
      testB: 0,
      testout: 0,
      bookList: []
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

    test2: function(a,b) {
      this.axios.get('http://127.0.0.1:8000/api/test2')
      .then((response) => {
        alert("rnm")
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    getPortfolio: function(a,b) {
      this.axios.get('http://127.0.0.1:8000/analysisTool/getPortfolio', {
        params: {
          startDate: "2019-06-01",
          endDate: "2019-09-01",
          books: ["jx","yz"]
        },
        paramsSerializer: params => {
          return this.$qs.stringify(params, {indices: false})
        }
      })
      .then((response) => {
        alert("ying")
        // console.log(response["data"]["performance"]["yz"])
        this.drawPortfolio(response["data"]["performance"]["yz"],"testChart1")
        console.log(response)
      })
      .catch((error) => {
        console.log(error)
      })
    },

    getMarket: function(a,b) {
      this.axios.get('http://127.0.0.1:8000/analysisTool/getMarket', {
        params: {
          startDate: "2020-03-01",
          endDate: "2020-06-01",
          ticker: "000002.SZ"
        }
      })
      .then((response) => {
        alert("ying")
        console.log(response)
        this.drawMarket(response["data"]["marketData"],"testChart4","testChart5")
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    getTransaction: function(a,b) {
      this.axios.get('http://127.0.0.1:8000/analysisTool/getTransaction', {
        params: {
          startDate: "2019-06-01",
          endDate: "2019-09-01",
          book: "jx",
          ticker: "000002.SZ"
        }
      })
      .then((response) => {
        alert("ying")
        console.log(response)
        this.drawTransaction(response["data"]["transactionData"],"testChart2","testChart3")

      })
      .catch(function (error) {
        console.log(error)
      })
    },

    drawPortfolio: function(dataInput,picID) {
      var option = {
        title: {
          text:"Portfolio Value"
        },
        tooltip: {},
        legend: {},
        xAxis: {type: "time"},
        yAxis: {},
        dataset: {
          source: eval(dataInput),
        },
        series:  [{
          type: 'line',
          encode: {
            x: "Date",
            y: "Value"
          }
        }],
      };
      console.log(option)
      echarts.init(document.getElementById(picID)).setOption(option);
    },

    drawTransaction: function(dataInput,picID1,picID2) {
      var option = {
        title: {
          text:"Return in percentage"
        },
        tooltip: {},
        legend: {},
        xAxis: {type: "time"},
        yAxis: {},
        dataset: {
          source: eval(dataInput),
        },
        series:  [{
          type: 'line',
          encode: {
            x: "Date",
            y: "PercentageReturn"
          }
        }],
      };
      echarts.init(document.getElementById(picID1)).setOption(option);

      var option = {
        title: {
          text:"Position"
        },
        tooltip: {},
        legend: {},
        xAxis: {type: "time"},
        yAxis: {},
        dataset: {
          source: eval(dataInput),
        },
        series:  [{
          type: 'bar',
          encode: {
            x: "Date",
            y: "Position"
          }
        }],
      };
      echarts.init(document.getElementById(picID2)).setOption(option);

    },

    drawMarket: function(dataInput,picID1,picID2) {
      var option = {
        title: {
          text:"Market Price"
        },
        tooltip: {},
        legend: {},
        xAxis: {type: "time"},
        yAxis: {},
        dataset: {
          source: eval(dataInput),
        },
        series:  [{
          type: 'candlestick',
          encode: {
            x: "Date",
            y: ["open","close","low","high"]
          }
        }],
      };
      echarts.init(document.getElementById(picID1)).setOption(option);

      var option = {
        title: {
          text:"Volume"
        },
        tooltip: {},
        legend: {},
        xAxis: {type: "time"},
        yAxis: {},
        dataset: {
          source: eval(dataInput),
        },
        series:  [{
          type: 'bar',
          encode: {
            x: "Date",
            y: ["Volume"]
          }
        }],
      };
      echarts.init(document.getElementById(picID2)).setOption(option);
    },

    getBookList: function(a,b) {
      this.axios.get('http://127.0.0.1:8000/analysisTool/getBookList')
      .then((response) => {

        console.log(response)
      })
      .catch((error) => {
        console.log(error)
      })
    },
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
