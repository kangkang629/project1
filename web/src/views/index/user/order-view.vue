<template>
  <div class="content-list">
    <div class="list-title">{{ lang.myorder[this.$store.state.language] }}</div>
    <a-tabs default-active-key="1" @change="onTabChange">
      <a-tab-pane key="1" :tab=lang.all[this.$store.state.language]>
      </a-tab-pane>
      <a-tab-pane key="2" :tab=lang.plspay[this.$store.state.language]>
      </a-tab-pane>
      <a-tab-pane key="3" :tab=lang.paid[this.$store.state.language]>
      </a-tab-pane>
    </a-tabs>
    <div v-if="this.$store.state.language === 'zh'" class="list-content">
      <div class="order-item-view" v-for="(item, index) in orderData" :key="index">
        <div class="header flex-view">
          <div class="left">
            <span class="text">订单号</span>
            <span class="num mg-4">#</span>
            <span class="num">{{item.order_number}}</span>
            <span class="time">{{item.order_time}}</span>
          </div>
          <div class="left">
            <span class="text">期望送达时间</span>
            <span class="num mg-4"></span>
            <a-date-picker
              :value="item.delivery_time"
              @change="dateOnChange($event, item)"
              format="YYYY-MM-DD HH:mm"
              :disabled-date="disabledDate"
              :disabled-time="disabledDateTime"
            />
          </div>
          <div class="right">
            <a-popconfirm
              v-if="item.status==='1'"
              title="确定取消订单？"
              ok-text="是"
              cancel-text="否"
              @confirm="handleCancel(item)"
            >
              <a-button type="primary" size="small" style="margin-right: 24px;">取消</a-button>
            </a-popconfirm>
            <span class="text">订单状态</span>
            <span class="state">{{item.status==='1'? '待支付': item.status === '2'? '已支付':'已取消'}}</span>
          </div>
        </div>
        <div class="content flex-view">
          <div class="left-list">
            <div class="list-item flex-view">
              <img :src="item.cover" class="thing-img">
              <div class="detail flex-between flex-view">
                <div class="flex-between flex-top flex-view">
                  <h2 class="name">{{item.title}}</h2>
                  <span class="count">x{{item.count}}</span>
                </div>
                <div class="flex-between flex-center flex-view">
                  <span class="type"></span>
                  <span class="price">¥{{item.price}}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="right-info">
            <p class="title">收货信息</p>
            <p class="name">{{item.receiver_name}}{{item.receiver_phone}}
            </p>
            <p class="text mg">{{item.receiver_address}}
            </p>
            <p class="title">快递单号</p>
            <p class="text">
            </p>
            <p class="title">备注信息</p>
            <p class="text">{{item.remark}}
            </p>
          </div>
        </div>
        <div class="bottom flex-view">
          <div class="left">
            <span class="text">共{{item.count}}件商品</span>
            <span class="open" @click="handleDetail(item.thing)">商品详情</span>
          </div>
          <div class="right flex-view">
            <span class="text">总计</span>
            <span class="num">¥ {{item.price * item.count}}</span>
            <span class="text">优惠</span>
            <span class="num">¥0</span>
            <span class="text">实际支付</span>
            <span class="money">¥ {{item.price * item.count}}</span>
          </div>
        </div>
      </div>
    </div>
    <div v-if="this.$store.state.language === 'en'" class="list-content">
      <div class="order-item-view" v-for="(item, index) in orderData" :key="index">
        <div class="header flex-view">
          <div class="left">
            <span class="text">Order No.</span>
            <span class="num mg-4">#</span>
            <span class="num">{{item.order_number}}</span>
            <span class="time">{{item.order_time}}</span>
          </div>
          <div class="left">
            <span class="text">Expected delivery time</span>
            <span class="num mg-4"></span>
            <a-config-provider :locale="en_US">
              <a-date-picker
                :value="item.delivery_time"
                :locale="en_US"
                @change="dateOnChange($event, item)"
                format="YYYY-MM-DD HH:mm"
                :disabled-date="disabledDate"
                :disabled-time="disabledDateTime"
              />
            </a-config-provider>
          </div>
          <div class="right">
            <a-popconfirm
              v-if="item.status==='1'"
              title="Cancel confirm？"
              ok-text="yes"
              cancel-text="no"
              @confirm="handleCancel(item)"
            >
              <a-button type="primary" size="small" style="margin-right: 24px;">Cancel</a-button>
            </a-popconfirm>
            <span class="text">Order Status</span>
            <span class="state">{{item.status==='1'? 'Unpaid': item.status === '2'? 'Paid':'Cancelled'}}</span>
          </div>
        </div>
        <div class="content flex-view">
          <div class="left-list">
            <div class="list-item flex-view">
              <img :src="item.cover" class="thing-img">
              <div class="detail flex-between flex-view">
                <div class="flex-between flex-top flex-view">
                  <h2 class="name">{{item.title}}</h2>
                  <span class="count">x{{item.count}}</span>
                </div>
                <div class="flex-between flex-center flex-view">
                  <span class="type"></span>
                  <span class="price">¥{{item.price}}</span>
                </div>
              </div>
            </div>
          </div>
          <div class="right-info">
            <p class="title">Receiving information</p>
            <p class="name">{{item.receiver_name}}{{item.receiver_phone}}
            </p>
            <p class="text mg">{{item.receiver_address}}
            </p>
            <p class="title">Tracking number</p>
            <p class="text">
            </p>
            <p class="title">Remark</p>
            <p class="text">{{item.remark}}
            </p>
          </div>
        </div>
        <div class="bottom flex-view">
          <div class="left">
            <span class="text">Total {{item.count}} of goods</span>
            <span class="open" @click="handleDetail(item.thing)">Goods Detail</span>
          </div>
          <div class="right flex-view">
            <span class="text">Total</span>
            <span class="num">¥ {{item.price * item.count}}</span>
            <span class="text">Preferential</span>
            <span class="num">¥0</span>
            <span class="text">Actual payment</span>
            <span class="money">¥ {{item.price * item.count}}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {listApi} from '@/api/index/order'
import moment from 'moment';
import {cancelOrderApi, deliveryApi} from '@/api/index/order'
import langData from '@/lang/lang.json'
import en_US from "ant-design-vue/es/locale/en_US";
export default {
  name: 'OrderView',
  computed: {
    en_US() {
      return en_US
    }
  },
  data () {
    return {
      orderData: ['', '', ''],
      orderStatus: '',
      timeVa: null,
      lang: langData
    }
  },
  mounted () {
    this.getOrderList()
    this.locale()
  },
  methods: {
    locale () {
      return this.$store.state.language;
    },
    onTabChange (key) {
      console.log(key)
      if (key === '1') {
        this.orderStatus = ''
      }
      if (key === '2') {
        this.orderStatus = '1'
      }
      if (key === '3') {
        this.orderStatus = '2'
      }
      this.getOrderList()
    },
    getOrderList () {
      this.loading = true
      let userId = this.$store.state.user.userId
      listApi({userId: userId, orderStatus: this.orderStatus}).then(res => {
        res.data.forEach((item, index) => {
          if (item.cover) {
            item.cover = this.$BASE_URL + item.cover
          }
        })
        this.orderData = res.data
        this.loading = false
      }).catch(err => {
        console.log(err)
        this.loading = false
      })
    },
    handleDetail (thingId) {
      // 跳转新页面
      let text = this.$router.resolve({name: 'detail', query: {id: thingId}})
      window.open(text.href, '_blank')
    },
    handleCancel (item) {
      cancelOrderApi({
        id: item.id
      }).then(res => {
        if (this.$store.state.language === 'zh'){
          this.$message.success('取消成功')
        } else {
          this.$message.success('Cancel success')
        }
        this.getOrderList()
      }).catch(err => {
        if (this.$store.state.language === 'zh') {
          this.$message.error(err.msg || '取消失败')
        } else {
          this.$message.error(err.msg || 'Cancel failed')
        }
      })
    },
    dateOnChange(val, item) {
      this.timeVa=moment(val).format('YYYY-MM-DD HH:mm')
      deliveryApi({
        id: item.id,
        time: this.timeVa
      }).then(res => {
        if (this.$store.state.language === 'zh') {
          this.$message.success('选择成功')
        } else {
          this.$message.success('select success')
        }

        this.getOrderList()
      }).catch(err => {
        if (this.$store.state.language === 'zh') {
          this.$message.error(err.msg || '取消失败')
        } else {
          this.$message.error(err.msg || 'cancel failed')
        }

      })
    },
    disabledDate(current) {
    //设置今天以前不可选，不包括今天
      return current && current < moment().subtract(1, 'days').endOf('day')
    },
    disabledDateTime() {
      return {
        disabledHours: () => this.range(0, 24).splice(4, 20),
        disabledMinutes: () => this.range(30, 60),
        disabledSeconds: () => [55, 56]
      }
    }
  }
}
</script>
<style scoped lang="less">
.flex-view {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
}

.content-list {
  -webkit-box-flex: 1;
  -ms-flex: 1;
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    line-height: 24px;
    height: 24px;
    margin-bottom: 4px;
  }
}

.order-item-view {
  background: #f7f9fb;
  border-radius: 4px;
  padding: 16px;
  margin-top: 12px;

  .header {
    border-bottom: 1px solid #cedce4;
    padding-bottom: 12px;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    font-size: 14px;

    .text {
      color: #6f6f6f;
    }

    .mg-4 {
      margin-left: 4px;
    }

    .num {
      font-weight: 500;
      color: #152844;
    }

    .num {
      font-weight: 500;
      color: #152844;
    }

    .time {
      margin-left: 16px;
      color: #a1adc5;
    }

    .state {
      color: #ff7b31;
      font-weight: 600;
      margin-left: 10px;
    }
  }

  .content {
    padding: 12px 0;
    overflow: hidden;

    .left-list {
      overflow: hidden;
      height: 132px;
      -webkit-box-flex: 2;
      -ms-flex: 2;
      flex: 2;
      padding-right: 16px;

      .list-item {
        height: 60px;
        margin-bottom: 12px;
        overflow: hidden;
        cursor: pointer;
      }

      .thing-img {
        width: 48px;
        height: 100%;
        margin-right: 12px;
      }

      .detail {
        -webkit-box-flex: 1;
        -ms-flex: 1;
        flex: 1;
        -webkit-box-orient: vertical;
        -webkit-box-direction: normal;
        -ms-flex-direction: column;
        flex-direction: column;
      }

      .flex-between {
        -webkit-box-pack: justify;
        -ms-flex-pack: justify;
        justify-content: space-between;
      }

      .flex-between {
        -webkit-box-pack: justify;
        -ms-flex-pack: justify;
        justify-content: space-between;
      }

      .flex-top {
        -webkit-box-align: start;
        -ms-flex-align: start;
        align-items: flex-start;
      }

      .name {
        color: #152844;
        font-weight: 600;
        font-size: 14px;
        line-height: 18px;
      }

      .count {
        color: #484848;
        font-size: 12px;
      }

      .flex-between {
        -webkit-box-pack: justify;
        -ms-flex-pack: justify;
        justify-content: space-between;
      }

      .flex-center {
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
      }

      .type {
        color: #6f6f6f;
        font-size: 12px;
      }

      .price {
        color: #ff7b31;
        font-weight: 600;
        font-size: 14px;
      }
    }

    .right-info {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      border-left: 1px solid #cedce4;
      padding-left: 12px;
      line-height: 22px;
      font-size: 14px;

      .title {
        color: #6f6f6f;
      }

      .name {
        color: #152844;
      }

      .text {
        color: #484848;
      }

      .mg {
        margin-bottom: 4px;
      }
    }
  }

  .bottom {
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    border-top: 1px solid #cedce4;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    font-size: 14px;
    padding-top: 14px;

    .text {
      color: #6f6f6f;
    }

    .open {
      color: #4684e2;
      margin-left: 8px;
      cursor: pointer;
    }

    .right {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
    }

    .text {
      color: #6f6f6f;
    }

    .num {
      color: #152844;
      margin: 0 40px 0 8px;
    }

    .money {
      font-weight: 600;
      font-size: 18px;
      color: #ff7b31;
      margin-left: 8px;
    }
  }

}

.order-item-view:first-child {
  margin-top: 16px;
}

</style>
