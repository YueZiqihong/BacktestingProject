<template>
  <div class="backtesting">
    <router-link to="/">
      <button class="btn btn-primary">Back to home page</button><br><br>
    </router-link>
    <div class="container">
    <div class="row">
      <div class="col-sm-3 text-center">
        <router-link to="/">
         <button class="btn btn-primary">Logout</button><br><br>
        </router-link>
        <img src="../assets/profile.jpg"><br><br>
        <a>{{username}}</a>
      </div>
      <div class="col-sm-8 text-center"><br><br><br>
        <div id="appin">
          <h4>Below is your personal report</h4><br><br>
          <button class="btn btn-secondary" @click="goBack">Go back to choose stock plan again</button>
        </div>
      </div>
    </div>
    </div><br>
    <div id="main" style="width: 1300px;height: 400px;"></div>
  </div>
</template>

<script>
import echarts from 'echarts'

export default {
  name: 'Report',
  data () {
    return {
      username: this.$route.query.Username,
      charts:'',
      opinionData1: [],
      opinionData2: [],
      xData: []
    }
  },
  mounted() {
    this.axios.get('http://127.0.0.1:8000/analysisTool/gettime', {
      params: {
        startDate: this.$route.query.StartDate,
        endDate: this.$route.query.EndDate,
        book: "ying"
      }
    })
    .then((response) => {
      // console.log(response)
      for(var i=0;i<response["data"]["dates"].length;i++){
        this.xData.push(response["data"]["dates"][i]["fields"]["trade_date"])
        this.opinionData1.push(Math.ceil(Math.random()*10))
        this.opinionData2.push(Math.ceil(Math.random()*10))
        this.$nextTick(() => {
          this.drawLine('main');
        })
      }
      // console.log(this.xData)
      // console.log(this.opinionData1)
    })
    .catch(function (error) {
      console.log(error)
    })

  },
  methods: {
    goBack: function(){
      this.$router.push({name:"StockPool",query:{Username : this.username}})
    },
    drawLine(id) {
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
          tooltip: {
              trigger: 'axis'
          },
          legend: {
              data: ['sta1','sta2']
          },
          grid: {
              left: '3%',
              right: '4%',
              bottom: '3%',
              containLabel: true
          },

          toolbox: {
              feature: {
                  saveAsImage: {}
              }
          },
          xAxis: {
              type: 'category',
              boundaryGap: false,
              data: this.xData

          },
          yAxis: {
              type: 'value'
          },

          series: [{
              name: 'sta1',
              type: 'line',
              data: this.opinionData1
          }, {name: 'sta2',
              type: 'line',
              data: this.opinionData2
          }]
      })
    }
   }
  }

</script>


<style scoped>
#main {
  margin: 0 auto;
    }

.container{
  background-color: bisque;
}

img{
  height:150px;
  width:200px;
}

</style>
