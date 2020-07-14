<template>
  <div class="portfolio">
    <div class="container">
      <h1>Portfolio Performance Review</h1>
    </div>
    <p>Here you can review the performance of your portfolio. If you have multiple accounts under your portfolio, you can either look at them separately or together.</p>
    <router-link to="/search">
      Other avaliable graphs<br><br>
    </router-link>
    <br><br>
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
    <p>Specify accounts:
      <el-select style="width:200px;" v-model="accountName" multiple placeholder="One or more">
  　     　   <el-option v-for="item in optList":key="item.value":value="item.value"></el-option>
      </el-select><br><br>
    </p>
    <el-button @click="search" style="margin: 2px;">Search</el-button>
    <div id="portfolioValue" style="width:1000px;height:600px;margin: auto;"></div>
  </div>
</template>

<script>
import echarts from 'echarts'

export default {
  name: 'Portfolio',
  data () {
    return {
      dateList: ["2019-06-01","2020-06-01"],
      accountName:[],
      optList: []
    }
  },
  mounted (){
    this.axios.get('http://127.0.0.1:8000/analysisTool/getBookList')
    .then((response) => {
      var plst=eval(response["data"]["books"])
      for(var i=0;i<plst.length;i++){
        this.optList.push({"value":plst[i]})
      }
    })
    .catch((error) => {
      console.log(error)
    })
  },
  methods: {
    search: function () {
      this.axios.get('http://127.0.0.1:8000/analysisTool/getPortfolio', {
              params: {
                startDate: this.dateList[0],
                endDate: this.dateList[1],
                books: this.accountName
              },
              paramsSerializer: params => {
                return this.$qs.stringify(params, {indices: false})
              }
            })
            .then((response) => {
              this.drawPortfolio(response["data"]["performanceTuple"],"portfolioValue")
              console.log(response)
            })
            .catch((error) => {
              console.log(error)
            })
    },

    drawPortfolio: function(dataInputObj,picID) {
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
           tooltip: {
             trigger: "item",
             triggerOn: 'mousemove|click',
           },
           xAxis: {
             type: "category",
           },
           yAxis: {
             type: "value",
             min: "dataMin",
             max: "dataMax",
           },
           legend: {},

           series: series
         };
         let chart = echarts.getInstanceByDom(document.getElementById(picID))
         if (chart) {
           echarts.dispose(chart)
         }
         chart = echarts.getInstanceByDom(document.getElementById(picID))
         if (!chart) {
           chart = echarts.init(document.getElementById(picID)).setOption(option);
         }
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
