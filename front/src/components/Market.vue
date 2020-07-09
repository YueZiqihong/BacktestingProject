<template>
  <div class="market">
    <div class="container">
      <h1>Market Viewer</h1>
      <p>Here you can search for market prices of a specific stock within specified time period. Candlestick views will be avaliable.</p>
      <router-link to="/search">
        Other avaliable graphs<br><br>
      </router-link>
    </div>

    <br><br><a>Set start date (yyyy-mm-dd)</a>
    <input type="text" v-model="startDate" placeholder="Input start date" />&nbsp; &nbsp;
    <a>Set end date (yyyy-mm-dd)</a>
    <input type="text" v-model="endDate" placeholder="Input end date" />&nbsp; &nbsp;
    <a>Set stock ticker</a>
    <input type="text" v-model="stockticker" placeholder="Input stock ticker" /><br><br>
    <button class="btn btn-secondary" @click="search">Search</button>&nbsp;<br><br>

    <div id="testChart1" style="width:500px;height:400px;display:inline;"></div>
    <div id="testChart2" style="width:500px;height:400px;display:inline;"></div>
  </div>
</template>

<script>
import echarts from 'echarts'

export default {
  name: 'Market',
  data () {
    return {
      startDate:"",
      endDate:"",
      stockticker:this.$route.params.id,
    }
  },
  methods: {
    search: function (){
      this.axios.get('http://127.0.0.1:8000/analysisTool/getMarket', {
        params: {
          startDate: this.startDate,
          endDate: this.endDate,
          ticker: this.stockticker
        }
      })
      .then((response) => {
        console.log(response)
        this.drawMarket(response["data"]["marketData"],"testChart1","testChart2")
      })
      .catch(function (error) {
        console.log(error)
      })
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
    }
  }
}
</script>

<style scoped>

.container{
  background-color: bisque;
}

img{
  height:150px;
  width:200px;
}

</style>
