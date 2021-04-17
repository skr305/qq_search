<template>

  <div class="total-wrp">
      测试页面
      <div class="my-test" v-if="CPI == 0" @click="switch_CPI()">
        CPI == 0
      </div>
      <div class="my-test" v-else @click="switch_CPI()">
        CPI == 1
      </div>
  </div>

</template>

<script>
import z_axios from '../util/axios_wrp' 

export default {
  name: 'HelloWorld',
  data() {
    return {
      CPI: 0
    }
  },
  methods: {
    switch_CPI() {
      this.CPI = this.CPI == 0 ? 1 : 0
    }
  },
  beforeMount() {
      let axios_config = {
           url: "/qq_search/test/",
           methods: "POST",
        }

      
      z_axios(axios_config)
      .then((res, rej) => {console.log(res || rej)})
  }


}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
 
</style>
