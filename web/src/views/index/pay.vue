<template>
  <div>
    <Header/>
    <div class="pay-content">
      <div class="title">{{ lang.ordersubmmit[this.$store.state.language] }}</div>
      <div class="text time-margin">
        <span>{{ lang.pls[this.$store.state.language] }} </span>
        <span class="time">{{ddlTime}}</span>
        <span> {{ lang.expiredorder[this.$store.state.language] }}</span>
      </div>
      <div class="text">{{ lang.payamount[this.$store.state.language] }}</div>
      <div class="price">
        <span class="num">{{ amount }}</span>
        <span>{{ lang.yuan[this.$store.state.language] }}</span>
      </div>
      <div class="pay-choose-view" style="">
        <div class="pay-choose-box flex-view">
          <div class="choose-box choose-box-active">
            <img src="@/assets/images/wx-pay-icon.svg">
            <span>{{ lang.winxipay[this.$store.state.language] }}</span>
          </div>
          <div class="choose-box">
            <img src="@/assets/images/ali-pay-icon.svg">
            <span>{{ lang.alipay[this.$store.state.language] }}</span>
          </div>
        </div>
        <div class="tips">{{ lang.paymethod[this.$store.state.language] }}</div>
        <button class="pay-btn pay-btn-active" @click="handlePay()">{{ lang.confirmpay[this.$store.state.language] }}</button>
      </div>
      <div class="pay-qr-view" style="display: none;">
        <div class="loading-tip" style="">{{ lang.qr[this.$store.state.language] }}</div>
        <div class="qr-box" style="display: none;">
          <div id="qrCode" class="qr">
            <img src="blob:https://www.ituring.com.cn/0928e0e9-71a0-4882-8df9-22367772364e" width="140" height="140">
          </div>
          <div class="tips">{{ lang.openweixin[this.$store.state.language] }}</div>
          <button class="pay-finish-btn">{{ lang.paycomplete[this.$store.state.language] }}</button>
          <button class="back-pay-btn">{{ lang.otherpay[this.$store.state.language] }}</button>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import Header from '@/views/index/components/header'
import Footer from '@/views/index/components/footer'
import langData from '@/lang/lang.json'

export default {
  components: {
    Footer,
    Header
  },
  data () {
    return {
      ddlTime: undefined,
      amount: undefined,
      lang: langData
    }
  },
  mounted () {
    this.amount = this.$route.query.amount
    this.locale()
    this.ddlTime = this.formatDate(new Date().getTime(), 'YY-MM-DD hh:mm:ss')

  },
  methods: {
    locale () {
      return this.$store.state.language;
    },
    handlePay () {
      if (this.$store.state.language === 'zh') {
        this.$message.warn('暂无支付功能')
      } else {
        this.$message.warn('No payment function currently available')
      }
    },
    formatDate (time, format = 'YY-MM-DD hh:mm:ss') {
      const date = new Date(time)

      const year = date.getFullYear(),
        month = date.getMonth() + 1,
        day = date.getDate() + 1,
        hour = date.getHours(),
        min = date.getMinutes(),
        sec = date.getSeconds()
      const preArr = Array.apply(null, Array(10)).map(function (elem, index) {
        return '0' + index
      })

      const newTime = format.replace(/YY/g, year)
        .replace(/MM/g, preArr[month] || month)
        .replace(/DD/g, preArr[day] || day)
        .replace(/hh/g, preArr[hour] || hour)
        .replace(/mm/g, preArr[min] || min)
        .replace(/ss/g, preArr[sec] || sec)

      return newTime
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

.pay-content {
  position: relative;
  margin: 120px auto 0;
  width: 500px;
  background: #fff;
  overflow: hidden;

  .title {
    color: #152844;
    font-weight: 500;
    font-size: 24px;
    line-height: 22px;
    height: 22px;
    text-align: center;
    margin-bottom: 11px;
  }

  .time-margin {
    margin: 11px 0 24px;
  }

  .text {
    height: 22px;
    line-height: 22px;
    font-size: 14px;
    text-align: center;
    color: #152844;
  }

  .time {
    color: #f62a2a;
  }

  .text {
    height: 22px;
    line-height: 22px;
    font-size: 14px;
    text-align: center;
    color: #152844;
  }

  .price {
    color: #ff8a00;
    font-weight: 500;
    font-size: 16px;
    height: 36px;
    line-height: 36px;
    text-align: center;

    .num {
      font-size: 28px;
    }
  }

  .pay-choose-view {
    margin-top: 24px;

    .choose-box {
      width: 140px;
      height: 126px;
      border: 1px solid #cedce4;
      border-radius: 4px;
      text-align: center;
      cursor: pointer;
    }

    .pay-choose-box {
      -webkit-box-pack: justify;
      -ms-flex-pack: justify;
      justify-content: space-between;
      max-width: 300px;
      margin: 0 auto;

      img {
        height: 40px;
        margin: 24px auto 16px;
        display: block;
      }
    }

    .tips {
      color: #6f6f6f;
      font-size: 14px;
      line-height: 22px;
      height: 22px;
      text-align: center;
      margin: 16px 0 24px;
    }

    .choose-box-active {
      border: 1px solid #4684e2;
    }

    .tips {
      color: #6f6f6f;
      font-size: 14px;
      line-height: 22px;
      height: 22px;
      text-align: center;
      margin: 16px 0 24px;
    }

    .pay-btn {
      cursor: pointer;
      background: #c3c9d5;
      border-radius: 32px;
      width: 104px;
      height: 32px;
      line-height: 32px;
      border: none;
      outline: none;
      font-size: 14px;
      color: #fff;
      text-align: center;
      display: block;
      margin: 0 auto;
    }

    .pay-btn-active {
      background: #4684e2;
    }
  }
}

</style>
