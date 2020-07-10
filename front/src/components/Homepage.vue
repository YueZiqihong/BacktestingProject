<template>
<div class="Homepage">
  <h1>Backtesting Tool By feizhai</h1>
  <h2>About This Page</h2>
  <p>This is a virtual backtesting system for China's stock share market. You can test your trading strtegies here and take advantage of the visualized transaction history to analyze your strategies.</p>

  <br>
  <p>Start writing up your strategy here:
    <router-link to="/backtesting">
      Get started
    </router-link>
  </p>

  <br>
  <h2>Upload your transaction history</h2>
  <p>Already have your transaction history and looking for a quick visualization tool? You can upload your transaction records as a csv file here:
    <router-link to="/upload">
      Upload
    </router-link>
    .
  </p>

  <br>
  <h2>Graphs</h2>
  <p>After you tested your strategy or you uploaded your transaction records, you can view the performance of both your <router-link to="/portfolio">portfolio</router-link> and <router-link to="/transaction">specific stock</router-link>. </p>
  <br>
  <p>For your reference, you can view stock prices <router-link to="/market">here</router-link></p>

  <el-button @click="test" style="margin: 2px;">test</el-button>

  <!-- <el-input v-model="testA" placeholder="a" style="display:inline-table; width: 30%; float:left"></el-input>
  <el-input v-model="testB" placeholder="b" style="display:inline-table; width: 30%; float:left"></el-input>
  <el-button type="primary" @click="test(testA,testB)" style="float:left; margin: 2px;">test</el-button>
  <p>{{testout}}</p>
  <el-button @click="test2(testA, testB)" style="float:left; margin: 2px;">test2</el-button>

  <el-button type="primary" @click="getPortfolio(testA,testB)" style="float:left; margin: 2px;">Portfolio</el-button>
  <br><br>
  <el-button type="primary" @click="getMarket(testA,testB)" style="float:left; margin: 2px;">Market</el-button>
  <el-button type="primary" @click="getTransaction(testA,testB)" style="float:left; margin: 2px;">Transaction</el-button>
  <el-button type="primary" @click="getBookList" style="float:left; margin: 2px;">Getlist</el-button>


  <div id="testChart1" style="width: 600px;height:400px;"></div>
  <br><br><br>
  <div id="testChart2" style="width: 600px;height:400px;"></div>
  <br><br><br>
  <div id="testChart3" style="width: 600px;height:400px;"></div>
  <br><br><br>
  <div id="testChart4" style="width: 600px;height:400px;"></div>
  <br><br><br>
  <div id="testChart5" style="width: 600px;height:400px;"></div>

  <br><br><br><br><br>

  <p>Choose Your stock plan and submit first, then go to next page choosing your strategy, start time and end time</p>
  <router-link to="/backtesting">
   <button class="btn btn-primary">Start Backtesting</button><br><br>
  </router-link>


  <br>


  <p>If you already have your transaction history and just want to visualize it, click here to upload your data as a csv file.</p>
  <router-link to="/upload">
    <button class="btn btn-primary">Upload page</button>&nbsp; &nbsp;
  </router-link>



  <div class="col-sm-8 text-center"><br><br><br>
    <div id="appin">
      <br><br>
      <h5>See related reports and graphs here</h5>
      <router-link to="/search">
        <button class="btn btn-primary">See graphs</button><br><br>
      </router-link>
    </div>
  </div> -->

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
        // this.drawPortfolio(response["data"]["performance"],"testChart1")
        this.drawPortfolio(response["data"]["dates"],response["data"]["performanceTuple"],"testChart1")
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

    drawPortfolio: function(dates,dataInputObj,picID) {
      var series = []
      for (let book in dataInputObj) {
        series.push({
          name: book,
          type: "line",
          data: eval(dataInputObj[book])
        })
      }
      var option = {
        title: {
          text:"Portfolio Value"
        },
        tooltip: {},
        legend: {},
        xAxis: {
          // type: "time",
          data: eval(dates)
        },
        yAxis: {},
        series: series
      };
      console.log(option)
      echarts.init(document.getElementById(picID)).setOption(option);
    },

    drawPortfoliobackup: function(dataInput,picID) {
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
