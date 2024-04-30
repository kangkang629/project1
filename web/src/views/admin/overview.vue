<template>

  <a-spin :spinning="showSpin">
    <div class="main">
      <a-row :gutter="[20,20]">
        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" :title=lang.allgoods[this.$store.state.language]>
            <a-tag color="blue" slot="extra">{{ lang.total[this.$store.state.language] }}</a-tag>
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ data.thing_count }}<span class="v-e">{{ lang.type[this.$store.state.language] }}</span></span>
                <a-icon type="profile" theme="twoTone" style="font-size: 24px;"/>
              </div>
              <div class="box-bottom">
                <span>{{ lang.thisweekadd[this.$store.state.language] }} {{ data.thing_week_count }} {{ lang.type[this.$store.state.language] }}</span>
              </div>
            </div>
          </a-card>
        </a-col>

        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" :title=lang.unpaidorder[this.$store.state.language]>
            <a-tag color="green" slot="extra">{{ lang.unpaid[this.$store.state.language] }}</a-tag>
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ data.order_not_pay_count }}<span class="v-e">{{ lang.order[this.$store.state.language] }}</span></span>
                <a-icon type="carry-out"  theme="twoTone" style="font-size: 24px;"/>
              </div>
              <div class="box-bottom">
                <span>{{ lang.total[this.$store.state.language] }} {{data.order_not_pay_p_count}} {{ lang.person[this.$store.state.language] }}</span>
              </div>
            </div>
          </a-card>
        </a-col>

        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" :title=lang.paidorder[this.$store.state.language]>
            <a-tag color="blue" slot="extra">{{ lang.paid[this.$store.state.language] }}</a-tag>
            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ data.order_payed_count }}<span class="v-e">{{ lang.order[this.$store.state.language] }}</span></span>
                <a-icon type="interaction" theme="twoTone" style="font-size: 24px;"/>
              </div>
              <div class="box-bottom">
                <span>{{ lang.total[this.$store.state.language] }} {{data.order_payed_p_count}} {{ lang.person[this.$store.state.language] }}</span>
              </div>
            </div>
          </a-card>
        </a-col>

        <a-col :sm="24" :md="12" :lg="6">
          <a-card size="small" :title=lang.cancelorder[this.$store.state.language]>
            <a-tag color="green" slot="extra">{{ lang.cancel[this.$store.state.language] }}</a-tag>

            <div class="box">
              <div class="box-top">
                <span class="box-value">{{ data.order_cancel_count }}<span class="v-e">{{ lang.order[this.$store.state.language] }}</span></span>
                <a-icon type="bell" theme="twoTone" style="font-size: 24px;"/>
              </div>
              <div class="box-bottom">
                <span>{{ lang.total[this.$store.state.language] }} {{data.order_cancel_p_count}} {{ lang.person[this.$store.state.language] }}</span>
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>

      <a-card :title=lang.visitoneweek[this.$store.state.language]>
        <div style="height: 300px;" ref="visitChart"></div>
      </a-card>



    </div>
  </a-spin>

</template>

<script>
import * as echarts from 'echarts'
import {listApi} from '@/api/admin/overview'
import storage from 'store'
import {ADMIN_TOKEN} from '@/store/constants'
import langData from '@/lang/lang.json'

export default {
  name: 'One',
  data () {
    return {
      showSpin: true,
      visitChart: undefined,
      barChart: undefined,
      pieChart: undefined,
      data: {
        order_rank_data: [],
        classification_rank_data: [],
        visit_data: []
      },
      lang: langData
    }
  },
  mounted () {
    // this.$store.commit('SET_NAME', 'zhangsan')
    // this.$store.dispatch('Login', 'linxiaomei')

    // console.log(this.$store.state.user.name)
    // console.log(this.$store.getters.name
    console.log(storage.get(ADMIN_TOKEN))
    this.list()
    const that = this
    window.onresize = function () { // resize
      that.visitChart.resize()
    }
    locale ()
  },
  methods: {
    locale () {
      return this.$store.state.language;
    },
    list () {
      listApi({}).then(res => {
        console.log(res.data)
        this.data = res.data
        this.initCharts()
        this.showSpin = false
      }).catch(err => {
        this.showSpin = false
        if (this.$store.state.language === 'zh') {
          this.$message.error(err.msg || '获取失败！')
        } else {
          this.$message.error(err.msg || 'query failed！')
        }
      })
    },
    initCharts () {
      const that = this
      setTimeout(function () {
        that.initVisitChart()
      }, 100)
    },
    initVisitChart () {
      let xData = []
      let uvData = []
      let pvData = []
      this.data.visit_data.forEach((item, index) => {
        xData.push(item.day)
        uvData.push(item.uv)
        pvData.push(item.pv)
      })
      this.visitChart = echarts.init(this.$refs.visitChart)
      let option = {
        title: {
          text: ''
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['IP', 'visit'],
          top: '90%',
          left: 'center'
        },
        grid: {
          top: '30px',
          left: '20px',
          right: '20px',
          bottom: '40px',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          axisLabel: {
            textStyle: {
              color: '#2F4F4F'
            }
          },
          axisLine: {
            lineStyle: {
              color: '#2F4F4F'
            }
          },
          // boundaryGap: false,
          data: xData
        },
        yAxis: {
          type: 'value',
          axisLine: {show: false},
          axisTick: {show: false},
          splitLine: {
            show: true, // 网格线
            lineStyle: {
              color: 'rgba(10, 10, 10, 0.1)',
              width: 1,
              type: 'solid'
            }
          }
        },
        series: [
          {
            name: 'IP',
            type: 'line',
            stack: 'Total',
            data: uvData
          },
          {
            name: 'visit',
            type: 'line',
            stack: 'Total',
            data: pvData
          }
        ]
      }
      this.visitChart.setOption(option)
    },
  }
}
</script>

<style lang="less" scoped>

.main {
  height: 100%;
  display: flex;
  gap:20px;
  flex-direction: column;

  .box {
    padding: 12px;
    display: flex;
    flex-direction: column;

    .box-top {
      display: flex;
      flex-direction: row;
      align-items: center;
    }
    .box-value {
      color: #000000;
      font-size: 32px;
      margin-right: 12px;
      .v-e {
        font-size: 14px;
      }
    }

    .box-bottom {
      margin-top: 24px;
      color: #000000d9;
    }
  }
}

</style>
