<template>
  <div class="backtesting">
    <div class="container">
    <h1>Customize your Strategy</h1>
    </div><br>
    <h2>Strategy</h2>

    <el-select style="width:200px;" v-model="strategy" placeholder="Select Strategy">
      <el-option v-for="item in optList":key="item":value="item"></el-option>
    </el-select>

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

    <br><br>
    <router-link to="/pool">
      <el-button style="margin: 2px;">Customize Stock Pool</el-button>
    </router-link>
    <br>
    <el-button @click="test" style="margin: 2px; background-color: rgb(255,111,97)">Start testing</el-button>

  </div>
</template>

<script>
export default {
  name: 'Backtesting',
  data () {
    return {
      strategy: "",
      dateList: ["2019-06-01","2020-06-01"],
      optList: ['random'],
      selectStrategy: "",
      poolInfo: this.$route.params.pool,
    }
  },
  methods: {
    test: function() {
      var stocks = []
      console.log(this.poolInfo.length)
      for (var i = 0; i < this.poolInfo.length; i++) {
        stocks.push(this.poolInfo[i]["ticker"])
      }

      var data = this.$qs.stringify({
        startDate: this.dateList[0],
        endDate: this.dateList[1],
        strategy: this.strategy,
        stockPool: stocks,
      }, {indices: false})

      this.axios.post('http://127.0.0.1:8000/analysisTool/startBacktesting', data)
      .then((response) => {


        if (response['data']['error_num'] == 0) {
          alert('Transaction data uploaded!')
        }
        else {
          alert(response['data']['msg']);
        }
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
        this.$message.error(error);
      })
    },
    getDefaultStrategy: function(){

    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
  /* text-align: left; */
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}

.container{
  background-color: bisque;
}

img{
  height:150px;
  width:200px;
}

</style>
