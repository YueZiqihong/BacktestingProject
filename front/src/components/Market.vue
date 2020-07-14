<template>
  <div class="market">
    <div class="container">
      <h1>Market Viewer</h1>
    </div>
    <p>Here you can search for market prices of a specific stock within specified time period. Candlestick views will be avaliable.</p>
    <router-link to="/search">
      Other avaliable graphs<br><br>
    </router-link>

    <div class="block">
      <span class="demonstration">Time period:</span>
      <el-date-picker
        v-model="dateList"
        type="daterange"
        value-format="yyyy-MM-dd"
        range-separator="To"
        start-placeholder="Start Date"
        end-placeholder="End Date">
      </el-date-picker>
    </div>
    <p>Stock ticker:
      <el-input
        size="medium"
        placeholder="Input stock ticker"
        v-model="ticker"
        clearable
        style="width:300px">
      </el-input>
    </p>
    <el-button @click="search" style="margin: 2px;">Search</el-button>

    <div id="stockPrice" style="width:1000px;height:600px;margin: auto;"></div>
    <div id="stockVolume" style="width:1000px;height:600px;margin: auto;"></div>
    <br><br><br>
  </div>
</template>

<script>
import echarts from 'echarts'

export default {
  name: 'Market',
  data () {
    return {
      dateList: ["2019-06-01","2020-06-01"],
      ticker: this.$route.params.id,
    }
  },
  methods: {
    search: function (){
      this.axios.get('http://127.0.0.1:8000/analysisTool/getMarket', {
        params: {
          startDate: this.dateList[0],
          endDate: this.dateList[1],
          ticker: this.ticker
        }
      })
      .then((response) => {
        console.log(response)
        this.drawMarket(response["data"]["marketData"],"stockPrice","stockVolume")
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
        tooltip: {
          trigger: "item",
          triggerOn: 'mousemove|click',
        },
        legend: {},
        xAxis: {type: "category"},
        yAxis: {
          type: "value",
          min: "dataMin",
          max: "dataMax",
        },
        dataZoom: [{
          start: 0,
          type: "inside"
        }, {
          start: 0
        }],
        dataset: {
          source: eval(dataInput),
        },
        series:  [{
          type: 'candlestick',
          encode: {
            x: "Date",
            y: ["open","close","low","high"],
            tooltip: ["open","close","low","high"],
          },

        }],
      };
      let chart = echarts.getInstanceByDom(document.getElementById(picID1))
      if (chart) {
        echarts.dispose(chart)
      }
      chart = echarts.getInstanceByDom(document.getElementById(picID1))
      if (!chart) {
        chart = echarts.init(document.getElementById(picID1)).setOption(option);
      }

      var option = {
        title: {
          text:"Volume"
        },
        tooltip: {
          trigger: "item",
          triggerOn: 'mousemove|click',
        },
        legend: {},
        xAxis: {type: "category"},
        yAxis: {
          type: "value",
          max: "dataMax",
        },
        dataZoom: [{
          start: 0,
          type: "inside"
        }, {
          start: 0
        }],
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
      chart = echarts.getInstanceByDom(document.getElementById(picID2))
      if (chart) {
        echarts.dispose(chart)
      }
      chart = echarts.getInstanceByDom(document.getElementById(picID2))
      if (!chart) {
        chart = echarts.init(document.getElementById(picID2)).setOption(option);
      }
    },

  },
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
