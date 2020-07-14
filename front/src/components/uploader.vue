<template>
  <div class="uploader">
    <h1>Uploading Page</h1>
    <div class="col-sm-8 text-center"><br><br><br>
      <p>If you already have your transaction records, you can upload your .csv file here directly.</p><br>
      <h2>File format</h2>
      <p>The csv file should be separated by comma; the first row is column names in the following order: book name, stock ticker,	date,	position,	value, average cost, return, percentage return. Data start at the second row.
      </p><br>
    </div>

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
        let config = {
          headers: {'Content-Type': 'multipart/form-data' }
        }
        let form = new FormData()
        form.append('file', param.file)
        console.log(form.get('file'));
        this.axios.post('http://127.0.0.1:8000/analysisTool/upload',form, config)
        .then((response) => {
          console.log(response)

          if (response['data']['error_num'] == 0) {
            alert('Transaction data uploaded!')
          }
          else {
            alert(response['data']['msg'])
          }
        })
        .catch((error) => {
          console.log(error)
        })
      }
      else{
        this.$message.error('Cannot upload empty file!');
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

.container{
  background-color: bisque;
}

img{
  height:150px;
  width:200px;
}
</style>
