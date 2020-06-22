<template>
<div class="hello">
  <h1>{{ msg }}</h1>
  <h2>Essential Links</h2>
  <ul>
    <li>
      <a href="https://www.google.com" target="_blank">
        谷歌
      </a>
    </li>
    <li>
      <router-link to="/backtesting">
        <button class="btn btn-default">Start testing</button>
      </router-link>
    </li>
  </ul>
  <h2>Test</h2>


  <!-- <el-row display="margin-top:10px">
    <el-input v-model="input" placeholder="请输入书名" style="display:inline-table; width: 30%; float:left"></el-input>
    <el-button type="primary" @click="addBook()" style="float:left; margin: 2px;">新增</el-button>
  </el-row>
  <el-row>
    <el-table :data="bookList" style="width: 100%" border>
      <el-table-column prop="id" label="编号" min-width="100">
        <template scope="scope"> {{ scope.row.pk }} </template>
      </el-table-column>
      <el-table-column prop="book_name" label="书名" min-width="100">
        <template scope="scope"> {{ scope.row.fields.book_name }} </template>
      </el-table-column>
      <el-table-column prop="add_time" label="添加时间" min-width="100">
        <template scope="scope"> {{ scope.row.fields.add_time }} </template>
      </el-table-column>
    </el-table>
  </el-row> -->

  <el-input v-model="testA" placeholder="a" style="display:inline-table; width: 30%; float:left"></el-input>
  <el-input v-model="testB" placeholder="b" style="display:inline-table; width: 30%; float:left"></el-input>
  <el-button type="primary" @click="test(testA,testB)" style="float:left; margin: 2px;">test</el-button>
  <p>{{testout}}</p>


</div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      msg: 'Welcome to Your Vue.js App',
      // input: '',
      // bookList: [],
      testA: 0,
      testB: 0,
      testout: 0,



    }
  },
  methods: {
    // addBook: function() {
    //   this.$http.get('http://127.0.0.1:8000/api/add_book?book_name=' + this.input)
    //     .then((response) => {
    //       var res = JSON.parse(response.bodyText)
    //       if (res.error_num == 0) {
    //         this.showBooks()
    //       } else {
    //         this.$message.error('新增书籍失败，请重试')
    //         console.log(res['msg'])
    //       }
    //     })
    // },
    // showBooks: function() {
    //   this.$http.get('http://127.0.0.1:8000/api/show_books')
    //     // alert("1");
    //     .then((response) => {
    //       var res = JSON.parse(response.bodyText)
    //       console.log(res)
    //       if (res.error_num == 0) {
    //         this.bookList = res['list']
    //       } else {
    //         this.$message.error('查询书籍失败')
    //         console.log(res['msg'])
    //       }
    //     })
    // },





    // test: function(a,b) {
    //   this.axios.get('http://127.0.0.1:8000/api/test', {
    //     params: {
    //     a: a,
    //     b: b
    //     }
    //   })
    //   .then(function (response){
    //     this.testout = response.data.testdata
    //     console.log(response)
    //   })
    //   .catch(function (error) {
    //     console.log(error)
    //   })
    // }

    test: function(a,b) {
      this.axios.get('http://127.0.0.1:8000/api/test', {
        params: {
        a: a,
        b: b
        }
      })
      .then((response) => {
        this.testout = response.data.testdata
        console.log(response)
      })
      .catch(function (error) {
        console.log(error)
      })
    }


      // ({
      //   method:"GET",
      //   url: 'http://127.0.0.1:8000/api/test',
      //   data: ({
      //     'a': a,
      //     'b': b
      //   }),
      // }).then((function(response) {
      //   if (response.error_num == 0) {
      //     this.testout = response['testdata']
      //   }
      //   else {
      //     alert('新增书籍失败，请重试')
      //     console.log(response['msg'])
      //   }
      // }))
    // }

  }
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
