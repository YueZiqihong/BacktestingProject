<template>
  <div class="transaction">
    <div class="container">
      <h1>Transaction Analysis Tool</h1>
    </div>
    <p>Here you can review the performance of specific stock you traded.</p>
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

    <p>Account:
      <el-select style="width:200px;" v-model="accountName" placeholder="Select account">
        <el-option v-for="item in optList":key="item.value":value="item.value"></el-option>
      </el-select>
    </p>

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
    <br><br><br>
    <div id="testChart1" style="width:500px;height:400px;display:inline;"></div>
    <div id="testChart2" style="width:500px;height:400px;display:inline;"></div>



  </div>





</template>

<script>
import echarts from 'echarts'

export default {
  name: 'Transaciton',
  data () {
    return {
      dateList:"",
      accountName:"",
      ticker:"",
      optList:[]
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
    search: function (){
      this.axios.get('http://127.0.0.1:8000/analysisTool/getTransaction', {
        params: {
          startDate: this.dateList[0],
          endDate: this.dateList[1],
          book: this.accountName,
          ticker: this.ticker
        }
      })
      .then((response) => {
        console.log(response)
        this.drawTransaction(response["data"]["transactionData"],"testChart1","testChart2")

      })
      .catch(function (error) {
        console.log(error)
      })
    },
    selectAccountName: function(event){
      this.accountName=event.target.value
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
