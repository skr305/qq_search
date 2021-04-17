<template>

  <div class="total-wrp" id="total-wrp">

    <!-- 搜索页面 -->
    <div class="wrp search-wrp"  v-if="(CPI == 0)">
        <div class="search">
          <!-- 选择器 -->
          <el-select class="HL-select" v-model="CSO" placeholder="搜索选项" >
            <el-option
              @change="switch_CSO(value)"
              v-for="item in CSO_LIST"
              :key="item.value"
              :label="item.label"
              :value="item.value">
            </el-option>
        </el-select>

          <!-- 搜索框 -->
          <div class="input-wrp">
              <el-input class="HL-input" v-model="CSK" placeholder="请输入内容"></el-input>
          </div>

          <!-- 搜索按钮 -->
          <div class="sr-btn-wrp">
            <el-button class="HL-sr" @click="send_search_request()">搜索</el-button>
          </div>
        </div>

        <!-- 结果列表 -->
        <div class="card-wrp">
            <el-card class="HL-card">
              <div slot="header">
                <span class="card-header-span">搜索结果</span>
              </div>
              <div class="card-content-wrp"  v-for="(record, index) in x" :key="record.qq_code*100+index">
                  <div class="card-content-word">QQ号:{{ record.qq_code }}</div>
                  <div class="card-content-word">昵称:{{ record.nick }}</div>
                  <div class="card-content-word">性别:{{ record.gender == 0 ? "男": "女"}}</div>
                  <div class="card-content-word">年龄:{{ record.age }}</div>
              </div>
            </el-card>
        </div>

        
    </div>

    <!-- ex图的对应说明部分 -->
    <div id="ex-ins">

    </div>
     <!-- ex图页面 -->
    <div class="wrp ex-wrp" id="ex-wrp">
      
    </div>

    <!-- 侧边切换按钮 -->
    <div class="sw-page-wrp" id="aside-btn" @click="switch_page_index()">
        <el-button type="primary" round icon="el-icon-star-off" class="HL-sw-page">切换为 {{ CPI == 0 ? "EX图" : "搜索"}} </el-button>      
    </div>

  </div>

</template>

<script>

import z_axios from '../util/axios_wrp'
import * as echarts from 'echarts';

export default {
  name: 'HelloWorld',
  data () {
    return {
      Type_Search_Response: {
        qq_code: "int",
        nick: "str",
        age: "int",
        gender: "int"
      },
      /** 未被转化的原始信息 */
      Type_Raw_Response: {
        QQNum: "int",
        Nick: "str",
        Age: "int",
        Gender: "int",
        Auth: "",
        QunNum: ""
      },

      /** 查询的返回结果 */
      x: [],

      /** 默认的查询选项是nick */
      CSO: 0,
      /** 搜索的key */
      CSK: "",
      /** 默认的页面是搜索页面 */
      CPI: 0,

      /**@CONST 
       * 用于放置选择器的表现 
       */
      CSO_LIST: [
        {label: "nick", value: 0},
        {label: "qq号", value: 1}
      ],
      
      /**@CONST 
       * 年龄列表
       */
      AL: [],

      /** 每个年龄段上的人数 */
      AA: [],

      /** 当前的ECHART实例 */
      IOV: {}
      
    }


  },

  methods: {
    /** 发送查询请求 */
    async send_search_request() {
      
      /** @PRIVATE
       * 用于作原始数据的适配器
       */
      let raw_adapter = (raw_data) => {
        let result = []
        for(let raw of raw_data) {
          result.push({
            qq_code: raw.QQNum,
            nick: raw.Nick,
            age: raw.Age,
            gender: raw.gender
          })
        }
        return result
      }

      let search_url = "/qq_search/" 
      + ( this.CSO == 0 ? "nick/" : "qq_code/" );

      let axios_config = {
        url: search_url,
        /** 携带搜索关键字 */
        params: {index: this.CSK},
        method: "POST"
      }

      z_axios(axios_config)
      .then((res) => {this.x = raw_adapter(res.data)})
      .catch((e) => {
        this.x = [{
          qq_code: "出错啦",
          nick: "出错啦", 
          age: "出错啦",
          gender: "出错啦"
        }]
        console.log(e);
      })

    },

    /** 切换页面 */
    switch_page_index() {
      this.CPI = this.CPI == 0 ? 1 : 0;
      if(this.CPI == 1) {
        /** 计算各年龄段人数 */
        this.compute_age_amounts()
        /** 初始化图表 */
        this.echarts_init()
        /** 注入对应的数据 */
        this.IOV.setOption(this.get_echarts_option())
      } else {
        /** 关闭图表 */
        this.echarts_dispose()
      }
      
    },

    /** 切换搜索选项 */
    switch_CSO(cso_index) {
      this.CSO = cso_index;
    },

    get_echarts_option() {
      /** echarts图的配置 */
      let option = {
        xAxis: {
            type: 'category',
            data: this.AL
        },
        yAxis: {
            type: 'value'
        },
        series: [{
            data: this.AA,
            type: 'line'
        }]
      };
      return option
    },

    echarts_init() {
      /** 初始化图表 */
      let echartsDOM = document.getElementById("ex-wrp")
      echartsDOM.style.height = "90vh"
      this.IOV = echarts.init(echartsDOM)

      /** 初始化图表说明 */
      let ec_ins = document.getElementById("ex-ins")
      ec_ins.innerHTML = "图表数据来源为搜索结果"
      let style_table = {
        textAlign: "Center",
        fontSize: "2rem",
        fontWeight: "100",
      } 
      ec_ins.style = style_table
    },

    echarts_dispose() {
      /** 卸载图表 */
      let echartsDOM = document.getElementById("ex-wrp")
      echartsDOM.style.height = "0"
      this.IOV.dispose()

      /** 卸载图表说明 */
      let ec_ins = document.getElementById("ex-ins")
      ec_ins.innerHTML = ""
    },


    compute_age_amounts() {
      /** 先把每个年龄段的人数请0 */
      for(let index in this.AA) {
        this.AA[index] = 0
      }

      /** 桶增 */
      for(let record of this.x) {
        this.AA[record.age]++
      }
    }


    
  },

  mounted() {
    /** 初始化AL和AA列表 */
    for(let i=0; i<121; i++) {
     this.AL.push(i+"岁")
    } 
    for(let i=0; i<121; i++) {
      this.AA.push(0)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .total-wrp {
    min-height: 26em;
  }


  .search, .card-content-wrp{
    display: flex;
    justify-content: space-around;
  }

  .card-content-wrp {
    /** 调记录条目的高度 */
    padding: 1.5em 0;

    /** 细的字体 */
    font-weight: 100;
  }


  /** 结果记录条目的框图 */
  .card-wrp {
    margin-top: 2rem;
  }

  .sw-page-wrp {
    position: fixed;
    right: 1em;
    top: 50%;
    transform: translate(0, -50%);
  }


  /** 调节搜索框的长度 */
  .HL-input {
    width: 30em  !important;

    /** 适应手机端 使得搜索框不至于太大 */
    max-width: 50vw;
  }
</style>
