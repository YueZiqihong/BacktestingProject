<template>
  <div id="stockpool">
    <h1>Setting Stock Pool</h1>
    <el-button @click="test()" style="float:left; margin: 2px;">test</el-button>
    <div class="container">
      <div class="col-sm-8 text-center"><br><br><br>
        <p>If you wish to operate your strategy within a certain pool, you can set the stock pool here.</p>
        <p>You can view your current stock pool below. When you are satisfied, you can return to your strategy.</p>
        <p>If you would like to view the price of any particular stock, search <router-link to="/market">here</router-link>, or click the ticker in the chart below.
        </p>
      </div>
    </div><br>
    <router-link to="/backtesting">
      <button class="btn btn-primary">Return to your strategy</button><br><br>
    </router-link>



    <div class="panel panel-primary">
      <h1>Your Customized Stock Pool</h1>
      <a>Stock plan</a>&nbsp; &nbsp; &nbsp;
        <select v-model="selectStockPlan" @change='getDefaultStockPlan($event)'>
          <option disabled value=''>--Select default plan--</option>
     　   <option v-for="item in optList">{{ item }}</option>
        </select>&nbsp; &nbsp;
      <a>or</a>&nbsp; &nbsp;
      <input type="text" v-model="iStockPlan" style='width:220px;' placeholder="Custom own plan with '-' or ','" />&nbsp; &nbsp;
      <button @click="customPlan">Custom</button>&nbsp; &nbsp;&nbsp; &nbsp;
      <button @click="reset">Reset</button><br><br>
      <input type="text" v-model="iSearch" style='width:220px;' placeholder="Search stock" />&nbsp; &nbsp;
      <button @click="search">Search</button>&nbsp; &nbsp;&nbsp; &nbsp;
      <div id='div-table-wrapper'>
        <div class='table-head-wrapper'>
          <table class="table table-bordered table-striped text-center">
            <thead>
              <tr>
                  <th>Serial number</th>
                  <th>Stock ticker</th>
                  <th>Trade date</th>
                  <th>Opening price</th>
                  <th>Closing price</th>
                  <th>High price</th>
                  <th>Low price</th>
                  <th>Volume</th>
                  <th>Change percent</th>
                  <th>Weight</th>
              </tr>
            </thead>
          </table>
        </div>
        <div class='table-body-wrapper' style='overflow:auto'>
          <table class='table table-bordered table-striped text-center' id='table-body'>
            <tbody   v-infinite-scroll="load"  infinite-scroll-disabled="disabled">
                <tr v-for ="(stock,index) in stocks.slice(0,count)">
                  <td>{{index+1}}</td>
                  <td><router-link :to="{name:'Market',params:{id:stock.ticker}}">{{stock.ticker}}</router-link></td>
                  <td>{{stock.tradeDate}}</td>
                  <td>{{stock.openPrice}}</td>
                  <td>{{stock.closePrice}}</td>
                  <td>{{stock.highPrice}}</td>
                  <td>{{stock.lowPrice}}</td>
                  <td>{{stock.volume}}</td>
                  <td>{{stock.changePercent}}</td>
                  <td>{{stock.weight}}</td>
                </tr>
            </tbody>
          </table>
          <p v-if="loading">loading...</p>
          <p v-if="noMore">no more</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data () {
    return {
      //stock: {'ticker': '', 'name': '', 'openPrice': '', 'closePrice': '', 'highPrice': '', 'lowPrice': '', 'volume':'', 'weight':''},
      selectStockPlan: '',
      iStockPlan: '',
      iSearch: '',
      count:4,
      loading:false,
      optList: ['Plan A', 'Plan B', 'Back to origin'],
      stocks: [
        {'ticker': '111111', 'tradeDate': '2020-06-01', 'openPrice': 23.5, 'closePrice':24.8 , 'highPrice': 24.8, 'lowPrice': 22.5, 'volume':200, 'changePercent':2.5, 'weight':0.35},
        {'ticker': '222222', 'tradeDate': '2020-06-01', 'openPrice': 148.5, 'closePrice': 139.2, 'highPrice': 149.5, 'lowPrice': 136.8, 'volume':1000, 'changePercent':3.5, 'weight':0.89},
        {'ticker': '333333', 'tradeDate': '2020-06-01', 'openPrice': 56.2, 'closePrice': 57.5, 'highPrice': 57.9, 'lowPrice': 56.1, 'volume':800, 'changePercent':1.5, 'weight':0.52},
        {'ticker': '444444', 'tradeDate': '2020-06-01', 'openPrice': 53.2, 'closePrice': 57.7, 'highPrice': 58.9, 'lowPrice': 49.1, 'volume':1800, 'changePercent':1.7, 'weight':0.72},
        {'ticker': '11', 'tradeDate': '2020-06-01', 'openPrice': 23.5, 'closePrice':24.8 , 'highPrice': 24.8, 'lowPrice': 22.5, 'volume':200, 'changePercent':2.5, 'weight':0.35},
        {'ticker': '22', 'tradeDate': '2020-06-01', 'openPrice': 148.5, 'closePrice': 139.2, 'highPrice': 149.5, 'lowPrice': 136.8, 'volume':1000, 'changePercent':3.5, 'weight':0.89},
        {'ticker': '33', 'tradeDate': '2020-06-01', 'openPrice': 56.2, 'closePrice': 57.5, 'highPrice': 57.9, 'lowPrice': 56.1, 'volume':800, 'changePercent':1.5, 'weight':0.52},
        {'ticker': '44', 'tradeDate': '2020-06-01', 'openPrice': 53.2, 'closePrice': 57.7, 'highPrice': 58.9, 'lowPrice': 49.1, 'volume':1800, 'changePercent':1.7, 'weight':0.72}
      ],
      backupstocks: [
        {'ticker': '111111', 'tradeDate': '2020-06-01', 'openPrice': 23.5, 'closePrice':24.8 , 'highPrice': 24.8, 'lowPrice': 22.5, 'volume':200, 'changePercent':2.5, 'weight':0.35},
        {'ticker': '222222', 'tradeDate': '2020-06-01', 'openPrice': 148.5, 'closePrice': 139.2, 'highPrice': 149.5, 'lowPrice': 136.8, 'volume':1000, 'changePercent':3.5, 'weight':0.89},
        {'ticker': '333333', 'tradeDate': '2020-06-01', 'openPrice': 56.2, 'closePrice': 57.5, 'highPrice': 57.9, 'lowPrice': 56.1, 'volume':800, 'changePercent':1.5, 'weight':0.52},
        {'ticker': '444444', 'tradeDate': '2020-06-01', 'openPrice': 53.2, 'closePrice': 57.7, 'highPrice': 58.9, 'lowPrice': 49.1, 'volume':1800, 'changePercent':1.7, 'weight':0.72},
        {'ticker': '11', 'tradeDate': '2020-06-01', 'openPrice': 23.5, 'closePrice':24.8 , 'highPrice': 24.8, 'lowPrice': 22.5, 'volume':200, 'changePercent':2.5, 'weight':0.35},
        {'ticker': '22', 'tradeDate': '2020-06-01', 'openPrice': 148.5, 'closePrice': 139.2, 'highPrice': 149.5, 'lowPrice': 136.8, 'volume':1000, 'changePercent':3.5, 'weight':0.89},
        {'ticker': '33', 'tradeDate': '2020-06-01', 'openPrice': 56.2, 'closePrice': 57.5, 'highPrice': 57.9, 'lowPrice': 56.1, 'volume':800, 'changePercent':1.5, 'weight':0.52},
        {'ticker': '44', 'tradeDate': '2020-06-01', 'openPrice': 53.2, 'closePrice': 57.7, 'highPrice': 58.9, 'lowPrice': 49.1, 'volume':1800, 'changePercent':1.7, 'weight':0.72}
      ]
    }
  },

  computed: {
    noMore () {
      return this.count >= 8
    },
    disabled () {
      return this.loading || this.noMore
    }
  },
  methods: {
    load () {
      this.loading = true
      setTimeout(() => {
        this.count += 1
        this.loading = false
      }, 2000)
    },
    getDefaultStockPlan: function (event) {
      this.stocks.splice(0,this.stocks.length)
      for(var i=0;i<this.backupstocks.length;i++){
        this.stocks.push(this.backupstocks[i])
      }
      if (event.target.value=="Plan A"){this.stocks=this.stocks.slice(0,3);}
      if (event.target.value=="Plan B"){this.stocks=this.stocks.slice(1,3);}
    },
    customPlan: function(){
      this.stocks.splice(0,this.stocks.length)
      for(var i=0;i<this.iStockPlan.split(',').length;i++){
        if (this.iStockPlan.split(',')[i].indexOf('-')==-1){
          this.stocks.push(this.backupstocks[parseInt(this.iStockPlan.split(',')[i])-1])
        }
        else{
          for(var j=parseInt(this.iStockPlan.split(',')[i].split('-')[0]);j<=parseInt(this.iStockPlan.split(',')[i].split('-')[1]);j++){
            this.stocks.push(this.backupstocks[j-1])
          }
        }
      }
    },
    reset: function() {
      this.stocks.splice(0,this.stocks.length)
      for(var i=0;i<this.backupstocks.length;i++){
        this.stocks.push(this.backupstocks[i])
      }
      this.iStockPlan=''
    },
    search: function(){
      if(this.iSearch==''){
        this.stocks.splice(0,this.stocks.length)
        for(var i=0;i<this.backupstocks.length;i++){
          this.stocks.push(this.backupstocks[i])
        }
      }
      else{
        this.stocks=[]
        for(var i=0;i<this.backupstocks.length;i++){
          if(this.backupstocks[i]["ticker"].indexOf(this.iSearch)!=-1){
            this.stocks.push(this.backupstocks[i])
          }
        }
        this.iSearch=''
      }
    },

    test: function() {
      this.axios.get('http://127.0.0.1:8000/analysisTool/getCurrentStockPrice')
      .then((response) => {

        console.log(response)
      })
      .catch((error) => {
        console.log(error)
      })
    },
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#div-table-wrapper {
	width: 1348px;
	margin-top: 10px;
	margin-bottom: 10px;
}

.table-head-wrapper {
  font-size: 5px;
	height: 50px;
	width: 100%;
}

.table-body-wrapper {

	height: 200px;
	overflow-y: auto;
	overflow-x: hidden;
	border-bottom: 1px solid #ddd;
	border-left: 1px solid #ddd;
	border-right: 1px solid #ddd;
}

th{
  width:240px;
}
td{
  width: 240px;
}

.container{
  background-color: bisque;
}

img{
  /* border-top:30px; */
  height:150px;
  width:200px;
}

</style>
