<template>
  <div class="portfolio">
    <router-link to="/">
      <button class="btn btn-primary">Back to home page</button><br><br>
    </router-link>
    <div class="container">
    <div class="row">
      <div class="col-sm-3 text-center">
        <br><br><img src="../assets/profile.jpg">
      </div>
      <div class="col-sm-8 text-center"><br><br><br>
        <div id="appin">
          <h4>Search portfolio with start time, end time and account name</h4><br><br>
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
    <a>Select account name</a>
    <el-select style="width:200px;" v-model="accountName" multiple placeholder="One or more">
　     　   <el-option v-for="item in optList":key="item.value":value="item.value"></el-option>
    </el-select><br><br>
    <!-- {{accountName}} -->
    <button class="btn btn-secondary" @click="search">Search</button><br><br>
    <div id="testChart1" style="width:500px;height:400px;display:inline;"></div>
  </div>
</template>

<script>
import echarts from 'echarts'

export default {
  name: 'Portfolio',
  data () {
    return {
      startDate:"",
      endDate:"",
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
      // console.log(this.optList)
    })
    .catch((error) => {
      console.log(error)
    })
  },
  methods: {
    search: function (){
      this.axios.get('http://127.0.0.1:8000/analysisTool/getPortfolio', {
              params: {
                startDate: this.startDate,
                endDate: this.endDate,
                books: this.accountName
              },
              paramsSerializer: params => {
                return this.$qs.stringify(params, {indices: false})
              }
            })
            .then((response) => {
              // console.log(response["data"]["performance"]["yz"])
              // this.drawPortfolio(response["data"]["performance"]["yz"],"testChart1")
              this.drawPortfolio(response["data"]["dates"],response["data"]["performanceTuple"],"testChart1")
              // console.log(response)
            })
            .catch((error) => {
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
         // console.log(option)
         echarts.init(document.getElementById(picID)).setOption(option);
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
