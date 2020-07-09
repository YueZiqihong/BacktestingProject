<template>
  <div class="transaction">
    <div class="container">

      <h1>Transaction Analysis Tool</h1>
      <p>Here you can review the performance of specific stock you traded.</p>
      <router-link to="/search">
        Other avaliable graphs<br><br>
      </router-link>
    </div>

    <br><br><a>Set start date (yyyy-mm-dd)</a>
    <input type="text" v-model="startDate" placeholder="Input start date" />&nbsp; &nbsp;
    <a>Set end date (yyyy-mm-dd)</a>
    <input type="text" v-model="endDate" placeholder="Input end date" />&nbsp; &nbsp;
    <br><br><a>Select account name (only one)</a>
    <select style="width:200px;" v-model="accountName" @change='selectAccountName($event)'>
　　        <option disabled value=''>--Select account name--</option>
　     　   <option v-for="item in optList">{{ item }}</option>
    </select>
    <a>Set stock ticker</a>
    <input type="text" v-model="stockticker" placeholder="Input stock ticker" />&nbsp; &nbsp;
    <button class="btn btn-secondary" @click="search">Search</button><br><br>
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
      startDate:"",
      endDate:"",
      accountName:"",
      stockticker:"",
      optList:[]
    }
  },
  mounted (){
    this.axios.get('http://127.0.0.1:8000/analysisTool/getBookList')
    .then((response) => {
      this.optList=eval(response["data"]["books"])
    })
    .catch((error) => {
      console.log(error)
    })
  },
  methods: {
    search: function (){
      this.axios.get('http://127.0.0.1:8000/analysisTool/getTransaction', {
        params: {
          startDate: this.startDate,
          endDate: this.endDate,
          book: this.accountName,
          ticker: this.stockticker
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
