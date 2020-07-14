<template>
  <div class="Homepage">
    <h1>Backtesting and Visualization Tool for Stock Trading</h1>
    <h2>About This Page</h2>
    <p>This is a virtual backtesting system for China's stock share market. You can test your trading strtegies here and take advantage of the visualized transaction history to analyze your strategies.</p>

    <br>
    <p>Start writing up your strategy here:
      <router-link to="/backtesting">
        Get started
      </router-link>
    </p>

    <br>
    <h2>Upload your transaction history</h2>
    <p>Already have your transaction history and looking for a quick visualization tool? You can upload your transaction records as a csv file here:
      <router-link to="/upload">
        Upload
      </router-link>
      .
    </p>

    <br>
    <h2>Graphs</h2>
    <p>After you tested your strategy or you uploaded your transaction records, you can view the performance of both your <router-link to="/portfolio">portfolio</router-link> and <router-link to="/transaction">specific stock</router-link>. </p>
    <br>.
    <p>For your reference, you can view stock prices <router-link to="/market">here</router-link></p>
  </div>
</template>

<script>
import echarts from 'echarts'

export default {
  name: 'HelloWorld',
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
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
