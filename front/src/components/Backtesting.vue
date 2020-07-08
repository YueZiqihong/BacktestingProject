<template>
  <div class="backtesting">
    <router-link to="/">
      <button class="btn btn-primary">Back to homepage</button><br><br>
    </router-link>
    <div class="container">
    <div class="row">
      <div class="col-sm-3 text-center">
        <br><img src="../assets/profile.jpg">
      </div>
      <div class="col-sm-8 text-center"><br><br><br>
        <div id="appin">
          <h4>Choose your strategy, start time and end time with your selected stock plan</h4><br><br>
        </div>
      </div>
    </div>
    </div><br>
    <h1>Backtesting Page</h1>
    <input type="text" id="strategy" v-model="strategy" placeholder="Write strategy" />&nbsp; &nbsp;
    <select style="width:200px;" v-model="selectStrategy" @change='getDefaultStrategy'>
　　        <option disabled value=''>--Select default strategy--</option>
　     　   <option v-for="item in optList">{{ item }}</option>
    </select>
    <br><br><input type="text" id="startDate" v-model="startDate" placeholder="Set start date" />&nbsp; &nbsp;<a>yyyy-mm-dd</a>
    <br><br><input type="text" id="endDate" v-model="endDate" placeholder="Set end date" />&nbsp; &nbsp;<a>yyyy-mm-dd</a>
    <br><br>
    <router-link to="/pool">
      <button class="btn btn-secondary">Select stock plan</button>
    </router-link>
    <button class="btn btn-secondary" @click="test">Start testing</button>



  </div>
</template>

<script>
export default {
  name: 'Backtesting',
  data () {
    return {
      msg: 'Backtesting page',
      strategy: "",
      startDate: "",
      endDate: "",
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

    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
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
