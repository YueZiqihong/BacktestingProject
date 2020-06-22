<template>
  <div class="userInput">
    <h1>Backtesting Page</h1>
    <p>yingyingying</p>
    <input type="text" id="strategy" v-model="strategy" placeholder="Write strategy" />
    <input type="text" id="startDate" v-model="startDate" placeholder="Set start date" />
    <input type="text" id="endDate" v-model="endDate" placeholder="Set end date" />
    <br>
    <p>二天在这做一个可以添加股票池的功能，默认是用市面上所有股票</p>
    <button @click="review">Start testing</button>
    <p id="response">{{response}}</p>
    <p id="report"></p>
  </div>
</template>

<script>
export default {
  name: 'Backtesting',
  data () {
    return {
      msg: 'Backtesting page',
      response: ""
    }
  },
  methods: {
    review: function() {
      alert("starting with " + this.strategy + " from " + this.startDate + " to " + this.endDate)
      this.response = "ok";
      if (this.response=="ok") {
        // alert("1");
        this.showReport();
      }
      else {
        this.response="rnm";
      }
    },
    showReport: function() {
      // alert("2");
      document.getElementById("report").innerHTML = "Report.jpg using" + this.strategy + " , " + this.startDate + " , " + this.endDate;
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
a {
  color: #42b983;
}
</style>
