<template>
  <div>
    <Header/>
    <section class="cart-page flex-view">
    <div class="left-flex">
      <div class="title flex-view">
        <h3>{{ lang.cartdetail[this.$store.state.language] }}</h3>
      </div>
      <div class="cart-list-view">
        <div class="list-th flex-view">
          <span class="line-1">{{ lang.ordername[this.$store.state.language] }}</span>
          <span class="line-2">{{ lang.price[this.$store.state.language] }}</span>
          <span class="line-5">{{ lang.number[this.$store.state.language] }}</span>
          <span class="line-6">{{ lang.operate[this.$store.state.language] }}</span>
        </div>
        <div class="list">
          <div class="items flex-view" v-for="(item, index) in cart_list" :key="index">
            <div class="book flex-view">
              <img :src="'http://127.0.0.1:8000/upload/' + item.cover">
              <h2>{{item.title}}</h2>
            </div>
            <div class="pay">¥{{item.price}}</div>
            <a-input-number v-model="item.number" :min="1" :max="10" @change="onCountChange"/>
              <img src="../../assets/images/delete-icon.svg" class="delete" @click="handleBack(item.id)">
          </div>
        </div>
      </div>
      <div class="title flex-view">
        <h3>{{ lang.remark[this.$store.state.language] }}</h3>
      </div>
      <textarea :value="remark" :placeholder=lang.remarkcontent[this.$store.state.language] class="remark">
    </textarea>
    </div>
    <div class="right-flex">
      <div class="title flex-view">
        <h3>{{ lang.address[this.$store.state.language] }}</h3>
        <span class="click-txt" @click="handleSelectAddress" v-if="receiver_address">{{ lang.selectaddress[this.$store.state.language] }}</span>
      </div>
      <div class="address-view">
        <div class="info" style="">
          <span>{{ lang.recipient[this.$store.state.language] }}</span>
          <span class="name">{{receiver_name}}
          </span>
          <span class="tel">{{receiver_phone}}
          </span>
        </div>
        <div class="address" v-if="receiver_address"> {{receiver_address}}</div>
        <div class="info" v-else>
          <span>{{ lang.noaddress[this.$store.state.language] }}</span>
          <span class="info-blue" @click="handleCreateAddress">{{ lang.newaddress[this.$store.state.language] }}</span>
        </div>
      </div>
      <div class="title flex-view">
        <h3>{{ lang.settlement[this.$store.state.language] }}</h3>
        <span class="click-txt">{{ lang.price[this.$store.state.language] }}</span>
      </div>
      <div class="price-view">
        <div class="price-item flex-view">
          <div class="item-name">{{ lang.goodstotal[this.$store.state.language] }}</div>
          <div class="price-txt">¥{{this.amount}}</div>
        </div>
        <div class="price-item flex-view">
          <div class="item-name">{{ lang.goodsdiscount[this.$store.state.language] }}</div>
          <div class="price-txt">¥0</div>
        </div>
        <div class="price-item flex-view">
          <div class="item-name">{{ lang.merdiscount[this.$store.state.language] }}</div>
          <div class="price-txt">¥0</div>
        </div>
        <div class="total-price-view flex-view">
          <span>{{ lang.total[this.$store.state.language] }}</span>
          <div class="price">
            <span class="font-big">¥{{this.amount}}</span>
          </div>
        </div>
        <div>
          <span class="text">Expected delivery time</span>
          <span class="num mg-4"></span>
          <a-config-provider :locale="en_US">
              <a-date-picker
                :value="delivery_time"
                @change="dateOnChange($event, item)"
                format="YYYY-MM-DD HH:mm"
                :disabled-date="disabledDate"
                :disabled-time="disabledDateTime"
              />
            </a-config-provider>
        </div>
        <div class="btns-view">
          <button class="btn buy" @click="handleBack()">{{ lang.backs[this.$store.state.language] }}</button>
          <button class="btn pay jiesuan" @click="handleJiesuan()">{{ lang.settlement[this.$store.state.language] }}</button>
        </div>
      </div>
    </div>
  </section>
  </div>
</template>

<script>
import Header from '@/views/index/components/header.vue'
import Footer from '@/views/index/components/footer.vue'
import AddAddress from '@/views/index/modal/add-address.vue'
import SelectAddress from '@/views/index/modal/select-address.vue'
import {createApi} from '@/api/index/order'
import {listApi as listAddressListApi} from '@/api/index/address'
import {listApi as listCartApi, delCart} from "@/api/index/cart"
import langData from '@/lang/lang.json'
import moment from "moment/moment";
import en_US from "ant-design-vue/es/locale/en_US";

export default {
  name: 'CartView',
  computed: {
    en_US() {
      return en_US
    }
  },
  components: {
    Footer,
    Header
  },
  data () {
    return {
      remark: undefined,
      amount: 0,
      receiver_name: undefined,
      receiver_phone: undefined,
      receiver_address: undefined,
      lang:langData,
      delivery_time: undefined,
      cart_list: []
    }
  },
  mounted () {
    this.locale()
    this.listAddressData()
    this.cartList()
  },
  methods: {
    locale () {
      return this.$store.state.language;
    },
    onCountChange(value){
      this.amount = 0
      for (let i = 0; i < this.cart_list.length; i++) {
        this.amount = this.amount + this.cart_list[i].number * this.cart_list[i].price
      }
    },
    cartList () {
      let userId = this.$store.state.user.userId
      listCartApi({userId: userId}).then(res => {
        this.cart_list = res.data
        for (let i = 0; i < this.cart_list.length; i++) {
          this.amount = this.amount + this.cart_list[i].number * this.cart_list[i].price
        }
      }).catch(err => {
        console.log(err)
      })
    },
    listAddressData () {
      let userId = this.$store.state.user.userId
      listAddressListApi({userId: userId}).then(res => {

        if (res.data.length > 0) {
          this.receiver_name = res.data[0].name
          this.receiver_phone = res.data[0].mobile
          this.receiver_address = res.data[0].desc
          res.data.forEach(item => {
            if (item.default) {
              this.receiver_name = item.name
              this.receiver_phone = item.mobile
              this.receiver_address = item.desc
            }
          })
        }
      }).catch(err => {
        console.log(err)
      })
    },

    handleSelectAddress () {
      if (this.$store.state.language === 'zh') {
        this.$dialog(
        SelectAddress,
        {
          on: {
            ok: form => {
              console.log(form)
              this.receiver_name = form.get('name')
              this.receiver_phone = form.get('mobile')
              this.receiver_address = form.get('desc')
            }
          }
        },
        {
          title: '选择地址',
          width: '480px',
          centered: true,
          bodyStyle: {
            maxHeight: 'calc(100vh - 200px)',
            overflowY: 'auto'
          }
        }
      )
      } else {
        this.$dialog(
        SelectAddress,
        {
          on: {
            ok: form => {
              console.log(form)
              this.receiver_name = form.get('name')
              this.receiver_phone = form.get('mobile')
              this.receiver_address = form.get('desc')
            }
          }
        },
        {
          title: 'Select Address',
          width: '480px',
          centered: true,
          bodyStyle: {
            maxHeight: 'calc(100vh - 200px)',
            overflowY: 'auto'
          }
        }
      )
      }
    },
    handleCreateAddress () {
      if (this.$store.state.language === 'zh') {
        this.$dialog(
        AddAddress,
        {
          on: {
            ok: form => {
              this.receiver_name = form.get('name')
              this.receiver_phone = form.get('mobile')
              this.receiver_address = form.get('desc')
            }
          }
        },
        {
          title: '新增地址',
          width: '480px',
          centered: true,
          bodyStyle: {
            maxHeight: 'calc(100vh - 200px)',
            overflowY: 'auto'
          }
        }
      )
      } else {
        this.$dialog(
        AddAddress,
        {
          on: {
            ok: form => {
              this.receiver_name = form.get('name')
              this.receiver_phone = form.get('mobile')
              this.receiver_address = form.get('desc')
            }
          }
        },
        {
          title: 'Add Address',
          width: '480px',
          centered: true,
          bodyStyle: {
            maxHeight: 'calc(100vh - 200px)',
            overflowY: 'auto'
          }
        }
      )
      }
    },
    handleBack (row) {
      delCart({cart_id: row}).then(res => {
        window.location.reload()
      }).catch(err => {
        console.log(err)
      })
    },
    handleJiesuan () {
      const formData = new FormData()
      let userId = this.$store.state.user.userId
      if (this.$store.state.language === 'zh') {
        if (!userId) {
          this.$message.warn('请先登录！')
          return
        }
        if (!this.receiver_name) {
          this.$message.warn('请选择地址！')
          return
        }
      } else {
        if (!userId) {
          this.$message.warn('Please log in first!')
          return
        }
        if (!this.receiver_name) {
          this.$message.warn('Please select an address!')
          return
        }
      }
      formData.append('user', userId)
      formData.append('type', 'cart')
      formData.append('cart_data', JSON.stringify(this.cart_list))
      formData.append('thing', this.id)
      formData.append('count', this.count)
      if (this.remark){
        formData.append('remark', this.remark)
      }
      formData.append('receiver_name', this.receiver_name)
      formData.append('receiver_phone', this.receiver_phone)
      formData.append('receiver_address', this.receiver_address)
      formData.append('delivery_time', this.delivery_time)
      console.log(formData)
      createApi(formData).then(res => {
        if (this.$store.state.language === 'zh') {
          this.$message.success('请支付订单')
        } else {
          this.$message.success('Please pay for the order')
        }
        this.$router.push({'name': 'pay', query: {'amount': this.amount}})
      }).catch(err => {
        if (this.$store.state.language === 'zh') {
          this.$message.error(err.msg || '失败')
        } else {
          this.$message.error(err.msg || 'Failed')
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
    },
    dateOnChange(val, item) {
      this.timeVa=moment(val).format('YYYY-MM-DD HH:mm')
      this.delivery_time = this.timeVa
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

.cart-page {
  width: 1024px;
  min-height: 50vh;
  margin: 100px auto;
}

.left-flex {
  -webkit-box-flex: 17;
  -ms-flex: 17;
  flex: 17;
  padding-right: 20px;
}

.title {
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  justify-content: space-between;
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;

  h3 {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    height: 26px;
    line-height: 26px;
    margin: 0;
  }
}

.cart-list-view {
  margin: 4px 0 40px;

  .list-th {
    height: 42px;
    line-height: 42px;
    border-bottom: 1px solid #cedce4;
    color: #152844;
    font-size: 14px;

    .line-1 {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      margin-right: 20px;
    }

    .line-2, .pc-style .cart-list-view .list-th .line-3, .pc-style .cart-list-view .list-th .line-4 {
      width: 65px;
      margin-right: 20px;
    }

    .line-5 {
      width: 80px;
      margin-right: 40px;
    }

    .line-6 {
      width: 28px;
    }
  }
}

.items {
  -webkit-box-align: center;
  -ms-flex-align: center;
  align-items: center;
  margin-top: 20px;

  .book {
    -webkit-box-flex: 1;
    -ms-flex: 1;
    flex: 1;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-right: 20px;
    cursor: pointer;

    img {
      width: 48px;
      margin-right: 16px;
      border-radius: 4px;
    }

    h2 {
      -webkit-box-flex: 1;
      -ms-flex: 1;
      flex: 1;
      font-size: 14px;
      line-height: 22px;
      color: #152844;
    }
  }

  .type {
    width: 65px;
    margin-right: 20px;
    color: #152844;
    font-size: 14px;
  }

  .pay {
    color: #ff8a00;
    font-weight: 600;
    font-size: 16px;
    width: 65px;
    margin-right: 20px;
  }

  .num-box {
    width: 80px;
    margin-right: 43px;
    border-radius: 4px;
    border: 1px solid #cedce4;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    height: 32px;
    padding: 0 4px;
  }

  .delete {
    margin-left: 36px;
    width: 24px;
    cursor: pointer;
  }
}

.mb-24 {
  margin-bottom: 24px;
}

.show-txt {
  color: #ff8a00;
  font-size: 14px;
}

.remark {
  width: 100%;
  background: #f6f9fb;
  border: 0;
  border-radius: 4px;
  padding: 6px 12px;
  //color: #152844;
  margin-top: 16px;
  resize: none;
  height: 56px;
  line-height: 22px;
}

.right-flex {
  -webkit-box-flex: 8;
  -ms-flex: 8;
  flex: 8;
  padding-left: 24px;
  border-left: 1px solid #cedce4;
}

.click-txt {
  color: #4684e2;
  font-size: 14px;
  cursor: pointer;
}

.address-view {
  margin: 12px 0 24px;

  .info {
    color: #909090;
    font-size: 14px;
    .info-blue {
      cursor: pointer;
      color: #4684e2;
    }
  }

  .name {
    color: #152844;
    font-weight: 500;
  }

  .tel {
    color: #152844;
    float: right;
  }

  .address {
    color: #152844;
    margin-top: 4px;
  }
}

.price-view {
  overflow: hidden;
  margin-top: 16px;

  .price-item {
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin-bottom: 8px;
    font-size: 14px;

    .item-name {
      color: #152844;
    }

    .price-txt {
      font-weight: 500;
      color: #ff8a00;
    }
  }

  .total-price-view {
    margin-top: 12px;
    border-top: 1px solid #cedce4;
    -webkit-box-pack: justify;
    -ms-flex-pack: justify;
    justify-content: space-between;
    -webkit-box-align: start;
    -ms-flex-align: start;
    align-items: flex-start;
    padding-top: 10px;
    color: #152844;
    font-weight: 500;

    .price {
      color: #ff8a00;
      font-size: 16px;
      height: 36px;
      line-height: 36px;
    }
  }

  .btns-view {
    margin-top: 24px;
    text-align: right;

    .buy {
      background: #fff;
      color: #4684e2;
    }

    .jiesuan {
      cursor: pointer;
      background: #4684e2;
      color: #fff;
    }

    .btn {
      cursor: pointer;
      width: 96px;
      height: 36px;
      line-height: 33px;
      margin-left: 16px;
      text-align: center;
      border-radius: 32px;
      border: 1px solid #4684e2;
      font-size: 16px;
      outline: none;
    }
  }

}

</style>
