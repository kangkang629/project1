<template>
  <div class="content-list">
    <div class="list-title">{{ lang.pushset[this.$store.state.language] }}</div>
    <div class="list-content">
      <div class="push-view">
        <div class="item flex-view">
          <div class="label">{{ lang.pushmail[this.$store.state.language] }}</div>
          <div class="right-box">
            <input type="text" class="input-dom" :placeholder=lang.entermail[this.$store.state.language] v-model="push_email">
          </div>
        </div>
        <div class="item flex-view">
          <div class="label">{{ lang.accpectemailmessage[this.$store.state.language] }}</div>
          <div class="right-box">
            <a-switch v-model="push_switch"/>
          </div>
        </div>
        <button class="save mg" @click="handleSave()">{{ lang.save[this.$store.state.language] }}</button>
      </div>
    </div>
  </div>
</template>

<script>
import {infoApi, updateApi} from '@/api/index/user'
import langData from '@/lang/lang.json'

export default {
  data () {
    return {
      push_email: undefined,
      push_switch: undefined,
      lang: langData
    }
  },
  mounted () {
    this.getUserInfo()
    this.locale()
  },
  methods: {
    locale () {
      return this.$store.state.language;
    },
    // 积分逻辑：积分加1
    getUserInfo () {
      this.loading = true
      let userId = this.$store.state.user.userId
      infoApi({id: userId}).then(res => {
        if (res.data) {
          this.push_email = res.data.push_email
          this.push_switch = res.data.push_switch
        }
        this.loading = false
      }).catch(err => {
        console.log(err)
        this.loading = false
      })
    },
    handleSave () {
      const reg = /^[a-zA-Z0-9][a-zA-Z0-9_]+\@[a-zA-Z0-9]+\.[a-zA-Z]{2,5}(\.[a-zA-Z]{2,5})*$/i

      if (!this.push_email.match(reg)) {
        if (this.$store.state.language === 'zh') {
          this.$message.warn('请输入正确的邮箱格式')
        } else {
          this.$message.warn('Please enter the correct email format')
        }
        
        return
      }

      let userId = this.$store.state.user.userId
      const formData = new FormData()
      if (this.push_email) {
        formData.append('push_email', this.push_email)
      }
      if (this.push_switch) {
        formData.append('push_switch', this.push_switch)
      }
      updateApi({id: userId}, formData).then(res => {
        if (res.data) {
          this.push_email = res.data.push_email
          this.push_switch = res.data.push_switch
        }
        if (this.$store.state.language === 'zh') {
          this.$message.success('保存成功')
        } else {
          this.$message.success('Save success')
        }
        
      }).catch(err => {
        console.log(err)
      })
    }
  }
}
</script>
<style scoped lang="less">
progress {
  vertical-align: baseline;
}

.flex-view {
  display: flex;
}

input, textarea {
  outline: none;
  border-style: none;
}

button {
  padding: 0;
}

.content-list {
  flex: 1;

  .list-title {
    color: #152844;
    font-weight: 600;
    font-size: 18px;
    //line-height: 24px;
    height: 48px;
    margin-bottom: 4px;
    border-bottom: 1px solid #cedce4;
  }
}

.push-view {
  .item {
    -webkit-box-align: center;
    -ms-flex-align: center;
    align-items: center;
    margin: 24px 0;

    .label {
      width: 100px;
      color: #152844;
      font-weight: 600;
      font-size: 14px;
    }

    .input-dom {
      background: #f8fafb;
      border-radius: 4px;
      width: 400px;
      height: 40px;
      line-height: 40px;
      font-size: 14px;
      color: #152844;
      padding: 0 12px;
    }
  }

  .mg {
    margin-left: 100px;
  }

  .save {
    cursor: pointer;
    background: #4684e2;
    border-radius: 32px;
    width: 96px;
    height: 32px;
    line-height: 32px;
    font-size: 14px;
    color: #fff;
    border: none;
    outline: none;
  }
}

.switch-view {
  position: relative;
  background: #a1adc5;
  border-radius: 32px;
  width: 48px;
  height: 28px;
  cursor: pointer;

  .circle {
    position: absolute;
    margin-left: 4px;
    top: 4px;
    width: 20px;
    height: 20px;
    background: #fff;
    border-radius: 50%;
  }

  .selected {
    right: 4px;
  }
}

.selected {
  background: #58b251;
}

</style>
