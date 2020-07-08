<template>
  <div class="market">
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
          <h4>Search stock candlestick chart with start time, end time and stock tinker</h4><br><br>
          <router-link to="/search">
            <button class="btn btn-primary">Back to search interface</button><br><br>
          </router-link>
        </div>
      </div>
    </div>
    </div>
    <br><br><a>Set start date (yyyy-mm-dd)</a>
    <input type="text" v-model="startDate" placeholder="Input start date" />&nbsp; &nbsp;
    <a>Set end date (yyyy-mm-dd)</a>
    <input type="text" v-model="endDate" placeholder="Input end date" />&nbsp; &nbsp;
    <a>Set stock tinker</a>
    <input type="text" v-model="stockTinker" placeholder="Input stock tinker" /><br><br>
    <button class="btn btn-secondary" @click="search">Search</button>&nbsp;<br><br>
    <!-- <div class="container"> -->
    <!-- <div class="row">
      <div class="col-sm-5 text-center">
        <div id="testChart1" style="width: 500px;height:400px;"></div>
      </div>
      <div class="col-sm-5 text-center">
        <div id="testChart2" style="width: 500px;height:400px;"></div>
      </div>
    </div>
    </div> -->
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
      stockTinker:""
    }
  },
  methods: {
    search: function (){
      this.axios.get('http://127.0.0.1:8000/analysisTool/getMarket', {
        params: {
          startDate: this.startDate,
          endDate: this.endDate,
          ticker: this.stockTinker
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
