<template>
   <div id="stockpool">
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
           <h4>Choose Your stock plan and submit first, then go to next page choosing your strategy, start time and end time</h4><br><br>
           <h5>Or you can search stock first</h5>
           <router-link to="/market">
             <button class="btn btn-primary">Search stock</button><br><br>
           </router-link>
         </div>
       </div>
     </div>
     </div><br>
     <router-link to="/backtesting">
       <button class="btn btn-primary">Continue setting your strategy</button>&nbsp; &nbsp;
     </router-link>

        <div class="panel panel-primary">
            <h3>Stock Pool</h3>
            <a>Stock plan</a>&nbsp; &nbsp; &nbsp;
            <select v-model="selectStockPlan" @change='getDefaultStockPlan($event)'>
    　　        <option disabled value=''>--Select default plan--</option>
    　     　   <option v-for="item in optList">{{ item }}</option>
            </select>&nbsp; &nbsp;
            <a>or</a>&nbsp; &nbsp;
            <input type="text" v-model="iStockPlan" style='width:220px;' placeholder="Custom own plan with '-' or ','" />&nbsp; &nbsp;
            <button @click="customPlan">Submit</button>&nbsp; &nbsp;&nbsp; &nbsp;
            <button @click="reset">Reset</button>
            <div id='div-table-wrapper'>
              <div class='table-head-wrapper'>
                <table class="table table-bordered table-striped text-center">
                  <thead>
                      <tr>
                          <th>Serial number</th>
                          <th>Stock tinker</th>
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
              <div class='table-body-wrapper'>
                <table class='table table-bordered table-striped text-center' id='table-body'>
                  <tbody>
                      <tr v-for ="(stock,index) in stocks">
                        <td>{{index+1}}</td>
                        <td>{{stock.tinker}}</td>
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
      //stock: {'tinker': '', 'name': '', 'openPrice': '', 'closePrice': '', 'highPrice': '', 'lowPrice': '', 'volume':'', 'weight':''},
      selectStockPlan: '',
      iStockPlan: '',
      optList: ['Plan A', 'Plan B', 'Back to origin'],
      stocks: [
        {'tinker': '111111', 'tradeDate': '2020-06-01', 'openPrice': 23.5, 'closePrice':24.8 , 'highPrice': 24.8, 'lowPrice': 22.5, 'volume':200, 'changePercent':2.5, 'weight':0.35},
        {'tinker': '222222', 'tradeDate': '2020-06-01', 'openPrice': 148.5, 'closePrice': 139.2, 'highPrice': 149.5, 'lowPrice': 136.8, 'volume':1000, 'changePercent':3.5, 'weight':0.89},
        {'tinker': '333333', 'tradeDate': '2020-06-01', 'openPrice': 56.2, 'closePrice': 57.5, 'highPrice': 57.9, 'lowPrice': 56.1, 'volume':800, 'changePercent':1.5, 'weight':0.52},
        {'tinker': '444444', 'tradeDate': '2020-06-01', 'openPrice': 53.2, 'closePrice': 57.7, 'highPrice': 58.9, 'lowPrice': 49.1, 'volume':1800, 'changePercent':1.7, 'weight':0.72}
      ],
      backupstocks: [
        {'tinker': '111111', 'tradeDate': '2020-06-01', 'openPrice': 23.5, 'closePrice':24.8 , 'highPrice': 24.8, 'lowPrice': 22.5, 'volume':200, 'changePercent':2.5, 'weight':0.35},
        {'tinker': '222222', 'tradeDate': '2020-06-01', 'openPrice': 148.5, 'closePrice': 139.2, 'highPrice': 149.5, 'lowPrice': 136.8, 'volume':1000, 'changePercent':3.5, 'weight':0.89},
        {'tinker': '333333', 'tradeDate': '2020-06-01', 'openPrice': 56.2, 'closePrice': 57.5, 'highPrice': 57.9, 'lowPrice': 56.1, 'volume':800, 'changePercent':1.5, 'weight':0.52},
        {'tinker': '444444', 'tradeDate': '2020-06-01', 'openPrice': 53.2, 'closePrice': 57.7, 'highPrice': 58.9, 'lowPrice': 49.1, 'volume':1800, 'changePercent':1.7, 'weight':0.72}
      ]
    }
  },
  // mounted: function(){
  //   this.axios.get('http://127.0.0.1:8000/api/stockPool')
  //   .then((response) => {
  //     console.log(response)
  //   })
  //   .catch(function (error) {
  //     console.log(error)
  //   })
  // },
  methods: {
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
    }
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
