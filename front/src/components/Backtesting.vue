<template>
  <div class="backtesting">
    <div class="container">
    <h1>Customize your Strategy</h1>
    </div><br>
    <h2>Strategy</h2>
    <el-input
      type="text"
      size="medium"
      placeholder="Write your strategy"
      v-model="strategy"
      clearable
      style="width:600px">
    </el-input>

    <!-- <el-select style="width:200px;" v-model="accountName" multiple placeholder="One or more">
　     <el-option v-for="item in optList":key="item.value":value="item.value"></el-option>
    </el-select><br><br> -->

    <select style="width:200px;" v-model="selectStrategy" @change='getDefaultStrategy'>
　　        <option disabled value=''>--Select default strategy--</option>
　     　   <option v-for="item in optList">{{ item }}</option>
    </select>

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
    <el-button @click="test" style="margin: 2px;">Start testing</el-button>




  </div>
</template>

<script>
export default {
  name: 'Backtesting',
  data () {
    return {
      strategy: "",
      dateList: "",
      optList: ['Strategy A', 'Strategy B'],
      selectStrategy: ""
    }
  },
  methods: {
    test: function() {
      this.$router.push({name:"Report",query:{StartDate : this.startDate,
                                              EndDate : this.endDate}})
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
