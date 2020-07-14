<template>
  <div id="stockpool">
    <div class="container">
      <h1>Setting Stock Pool</h1>
    </div><br>
    <div class="col-sm-8 text-center"><br><br><br>
      <p>If you wish to operate your strategy within a certain pool, you can set the stock pool here.</p>
      <p>You can view your current stock pool below.</p>
      <p>If you would like to view the price of any particular stock, search <router-link to="/market">here</router-link>, or click the ticker in the chart below.
      </p>
      <p>When you are satisfied, you can return to your strategy. Unsaved progress will be lost!</p>
    </div>
    <router-link :to="{name: 'backtesting', params: {pool: this.stocks}}">
      <el-button style="background-color: yellow" >Confirm and return to your strategy</el-button>
    </router-link>


    <div class="panel panel-primary">
      <h1>Your Customized Stock Pool</h1>
      <a>Stock plan</a>&nbsp; &nbsp; &nbsp;
        <select v-model="selectStockPlan" @change='getDefaultStockPlan($event)'>
          <option disabled value=''>--Select default plan--</option>
     　   <option v-for="item in optList">{{ item }}</option>
        </select>&nbsp; &nbsp;
      <a>or</a>&nbsp; &nbsp;
      <input type="text" v-model="iStockPlan" style='width:300px;' placeholder="Add or delete stock inputing stock ticker" />&nbsp; &nbsp;
      <button @click="addPlan">Add</button>&nbsp; &nbsp;&nbsp; &nbsp;
      <button @click="deletePlan">Delete</button>&nbsp; &nbsp;&nbsp; &nbsp;
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
                  <td>{{stock.date}}</td>
                  <td>{{stock.open}}</td>
                  <td>{{stock.close}}</td>
                  <td>{{stock.high}}</td>
                  <td>{{stock.low}}</td>
                  <td>{{stock.volume}}</td>
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
      selectStockPlan: '',
      iStockPlan: '',
      iSearch: '',
      count:10,
      loading:false,
      optList: ['All Stocks', 'Hushen 300', 'Clear All', 'Back to origin'],
      stocks: [],
      backupstocks: [],
      defaultstocks: ['600208.SH','600219.SH','600221.SH','600233.SH','600276.SH','600297.SH','600299.SH','600309.SH','600176.SH','600346.SH','600362.SH','600369.SH','600372.SH','600383.SH','600390.SH','600398.SH','600498.SH','600519.SH','600332.SH','600583.SH','600585.SH','600588.SH','600606.SH','600637.SH','600566.SH','600660.SH','600663.SH','600674.SH','600690.SH','600703.SH','600705.SH','600733.SH','600655.SH','600760.SH','600795.SH','600809.SH','600816.SH','600837.SH','600848.SH','601607.SH','600741.SH','600886.SH','600887.SH','600893.SH','600535.SH','600516.SH','600050.SH','600522.SH','600030.SH','600867.SH','600570.SH','600436.SH','600031.SH','600271.SH','600029.SH','600352.SH','600489.SH','600487.SH','600547.SH','600015.SH','600406.SH','600004.SH','600340.SH','000100.SZ','600438.SH','002001.SZ','002007.SZ','002008.SZ','002010.SZ','600482.SH','002024.SZ','002027.SZ','002032.SZ','600027.SH','002044.SZ','002050.SZ','600900.SH','002153.SZ','002146.SZ','600048.SH','601006.SH','601111.SH','002081.SZ','600018.SH','601398.SH','601988.SH','002120.SZ','601166.SH','601318.SH','000338.SZ','601628.SH','601328.SH','601600.SH','601919.SH','002142.SZ','601009.SH','601088.SH','002304.SZ','601857.SH','601390.SH','002202.SZ','601601.SH','300024.SZ','601899.SH','601898.SH','601186.SH','002230.SZ','002236.SZ','002252.SZ','002241.SZ','601901.SH','601878.SH','002673.SZ','601198.SH','601288.SH','601838.SH','601998.SH','601229.SH','601162.SH','601668.SH','002271.SZ','601788.SH','601766.SH','601633.SH','601727.SH','002294.SZ','600999.SH','601888.SH','601989.SH','002311.SZ','601618.SH','601117.SH','300003.SZ','601997.SH','300017.SZ','300015.SZ','300033.SZ','002352.SZ','601688.SH','002410.SZ','300059.SZ','002411.SZ','002415.SZ','002422.SZ','002456.SZ','300070.SZ','601012.SH','002466.SZ','002460.SZ','300124.SZ','601018.SH','002468.SZ','601377.SH','601877.SH','002475.SZ','601818.SH','300122.SZ','600998.SH','002493.SZ','600958.SH','300136.SZ','300142.SZ','002508.SZ','600926.SH','600919.SH','300144.SZ','000166.SZ','002736.SZ','601211.SH','601933.SH','601336.SH','002558.SZ','601216.SH','601992.SH','603156.SH','002594.SZ','002601.SZ','002607.SZ','002602.SZ','002555.SZ','601669.SH','601225.SH','601555.SH','601800.SH','601360.SH','002624.SZ','603993.SH','603288.SH','300347.SZ','002714.SZ','002773.SZ','601169.SH','002179.SZ','601238.SH','601808.SH','000333.SZ','600023.SH','002739.SZ','601939.SH','601021.SH','601828.SH','601985.SH','603986.SH','603160.SH','300433.SZ','603799.SH','601212.SH','600977.SH','603019.SH','300413.SZ','300408.SZ','601881.SH','603833.SH','002841.SZ','603501.SH','300498.SZ','601108.SH','601155.SH','001979.SZ','603260.SH','600025.SH','600968.SH','002939.SZ','002945.SZ','002958.SZ','601577.SH','600928.SH','002916.SZ','601066.SH','601236.SH','603259.SH','601319.SH','601298.SH','002938.SZ','601698.SH','600989.SH','601138.SH','603899.SH','000415.SZ','000423.SZ','000425.SZ','000538.SZ','000568.SZ','000413.SZ','000625.SZ','000627.SZ','000629.SZ','000630.SZ','000651.SZ','000656.SZ','000661.SZ','000671.SZ','000703.SZ','000709.SZ','000723.SZ','000725.SZ','000728.SZ','000596.SZ','000776.SZ','000783.SZ','000786.SZ','000858.SZ','000876.SZ','000895.SZ','000898.SZ','000938.SZ','000961.SZ','000768.SZ','600000.SH','000002.SZ','000001.SZ','000069.SZ','000157.SZ','000063.SZ','600009.SH','600010.SH','600011.SH','600016.SH','600019.SH','600028.SH','600036.SH','600038.SH','600061.SH','000963.SZ','600068.SH','600085.SH','600089.SH','600100.SH','600104.SH','600109.SH','600111.SH','600115.SH','600118.SH','600153.SH','600170.SH','600066.SH','600177.SH','600183.SH','600188.SH','600196.SH'].sort()
    }
  },
  computed: {
    noMore () {
      return this.count >= this.stocks.length
    },
    disabled () {
      return this.loading || this.noMore
    }
  },
  mounted (){
    this.axios.get('http://127.0.0.1:8000/analysisTool/getCurrentStockPrice')
    .then((response) => {
      this.stocks=eval(response["data"]["price"])
      this.backupstocks=eval(response["data"]["price"])
    })
    .catch((error) => {
      console.log(error)
    })
  },
  methods: {
    load () {
      this.loading = true
      setTimeout(() => {
        this.count += 10
        this.loading = false
      }, 1000)
    },
    getDefaultStockPlan: function (event) {
      this.stocks.splice(0,this.stocks.length)
      for(var i=0;i<this.backupstocks.length;i++){
        this.stocks.push(this.backupstocks[i])
      }
      if (event.target.value=="Hushen 300"){
        this.stocks=[]
        var flag=-1
        for(var i=0;i<this.defaultstocks.length;i++){
          for(var j=flag+1;j<this.backupstocks.length;j++){
            if(this.defaultstocks[i]==this.backupstocks[j]["ticker"]){
              this.stocks.push(this.backupstocks[j])
              flag=j
              break
            }
          }
        }        
      }
      if (event.target.value=="Clear All"){
        this.stocks=[]
      }
    },
    addPlan: function(){
      var flag=0
      var fflag=0
      for(var i=0;i<this.stocks.length;i++){
        if(this.stocks[i]['ticker']==this.iStockPlan){flag=1}
      }
      if(flag==1){alert("You already choose this stock!")}
      else{
        for(var j=0;j<this.backupstocks.length;j++){
          if(this.backupstocks[j]['ticker']==this.iStockPlan){
              fflag=1
              break
            }
          }
        if(fflag==0){alert("Wrong stock ticker!")}
        else{
          this.stocks.push(this.backupstocks[j])
          }
      }
        console.log(this.stocks)
      this.iStockPlan=''
    },
    deletePlan: function(){
      var flag=0
      for(var i=0;i<this.stocks.length;i++){
        if(this.stocks[i]['ticker']==this.iStockPlan){
          this.stocks.splice(i,1)
          flag=1
          break
        }
      }
      if(flag==0){alert("There is no such stock in your stock plan!")}
      this.iStockPlan=''
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
      }
      this.iSearch=''
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
