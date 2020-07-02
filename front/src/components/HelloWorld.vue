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
  <el-button @click="test2(testA, testB)" style="float:left; margin: 2px;">test2</el-button>

  <el-button type="primary" @click="getPortfolio(testA,testB)" style="float:left; margin: 2px;">Portfolio</el-button>
  <br><br>
  <el-button type="primary" @click="getMarket(testA,testB)" style="float:left; margin: 2px;">Market</el-button>
  <el-button type="primary" @click="getTransaction(testA,testB)" style="float:left; margin: 2px;">Transaction</el-button>
  <br>
  <el-button type="primary" @click="drawLine" style="float:left; margin: 2px;">chart</el-button>
  <div id="testChart1" style="width: 600px;height:400px;"></div>
  <br><br><br>
  <div id="testChart2" style="width: 600px;height:400px;"></div>
  <br><br><br>
  <div id="testChart3" style="width: 600px;height:400px;"></div>

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
          startDate: "2020-03-01",
          endDate: "2020-06-01",
          books: ["jx","yz"]
        },
        paramsSerializer: params => {
          return this.$qs.stringify(params, {indices: false})
        }
      })
      .then((response) => {
        alert("ying")
        // console.log(response["data"]["performance"]["yz"])
        this.drawLine(response["data"]["performance"]["yz"],"testChart1")
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    getMarket: function(a,b) {
      this.axios.get('http://127.0.0.1:8000/analysisTool/getMarket', {
        params: {
          startDate: a,
          endDate: b,
          ticker: "000002.SZ"
        }
      })
      .then((response) => {
        alert("ying")
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    getTransaction: function(a,b) {
      this.axios.get('http://127.0.0.1:8000/analysisTool/getTransaction', {
        params: {
          startDate: "2020-03-01",
          endDate: "2020-06-01",
          book: "jx",
          ticker: "000002.SZ"
        }
      })
      .then((response) => {
        alert("ying")
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      })
    },

    drawLine: function(dataInput,picID) {
      var option = {
        title: {
          text:"yingying"
        },
        tooltip: {},
        legend: {},
        xAxis: {type: "time"},
        yAxis: {},
        dataset: {
          // 这里指定了维度名的顺序，从而可以利用默认的维度到坐标轴的映射。
          // 如果不指定 dimensions，也可以通过指定 series.encode 完成映射，参见后文。
          dimensions: ["trade_day_id__trade_date","total_value"],
          source: eval(dataInput),
        },
        series:  [{type: 'line'}],
      };
      console.log(option)
      echarts.init(document.getElementById(picID)).setOption(option);
    },

    drawTransaction: function(dataInput,picID1,picID2) {

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
