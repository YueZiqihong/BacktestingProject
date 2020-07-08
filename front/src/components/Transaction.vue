<template>
  <div class="transaction">
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
          <h4>Search transaction analysis with start time, end time, account name and stock tinker</h4><br><br>
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
    <br><br><a>Select account name (only one)</a>
    <select style="width:200px;" v-model="accountName" @change='selectAccountName($event)'>
　　        <option disabled value=''>--Select account name--</option>
　     　   <option v-for="item in optList">{{ item }}</option>
    </select>
    <a>Set stock tinker</a>
    <input type="text" v-model="stockTinker" placeholder="Input stock tinker" />&nbsp; &nbsp;
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
      stockTinker:"",
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
          ticker: this.stockTinker
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
