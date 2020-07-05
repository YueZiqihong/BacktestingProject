<template>
<div class="uploader">
  <h1>Backtesting Page</h1>
  <p>yingyingying</p>
  <router-link to="/">
    <button class="btn btn-default">Home</button>
  </router-link>

  <el-upload
    class="upload-demo"
    ref="upload"
    drag
    action="fake"
    :http-request="importCsv"
    :multiple="false"
    :limit="1"
    :auto-upload="false"
    :on-change="handleChange"
    :headers="{'Content-Type': 'multipart/form-data' }"
    :show-file-list="true"
    >
    <el-button slot="trigger" size="small" type="primary">Select your csv file</el-button>
    <el-button style="margin-left: 10px;" size="small" type="success" @click="submitUpload">Upload</el-button>
  </el-upload>


</div>
</template>

<script>

export default {
  name: 'uploader',
  data() {
    return {
      file: {},
      csvVisible: false,
      csvTitle: 'importcsv'
    }
  },
  methods: {
    handleChange(file, fileList) {
      this.fileList = fileList.slice(-1);
    },

    importCsv: function (param) {
      if(param.file.length != 0){
        // alert(2)
        let config = {
          headers: {'Content-Type': 'multipart/form-data' }
        }
        let form = new FormData()

        form.append('file', param.file)
        console.log(form.get('file'));

        this.axios.post('http://127.0.0.1:8000/analysisTool/upload',form,config)
        .then((response) => {
          console.log(response)



          if (response['error_num'] == 0) {
            this.$message({
              message: 'Transaction data uploaded!',
              type: 'success'
            });
          }
          else {
            this.$message.error(response['msg']);
          }

        })
        .catch((error) => {
          console.log(error)
        })
      }
      else{
        this.$message.error('上传文件不能为空');
      }
    },



    submitUpload() {
      this.$refs.upload.submit();
    },



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
