<template>
  <div class="content-list">
    <div class="list-title">{{ lang.accountsafe[this.$store.state.language] }}</div>
    <div class="list-content">
      <div class="safe-view">
        <div class="safe-info-box">
          <div class="item flex-view">
            <div class="label">{{ lang.accountsafelevel[this.$store.state.language] }}</div>
            <div class="right-box flex-center flex-view">
              <div class="safe-text">{{ lang.lowrisk[this.$store.state.language] }}</div>
              <progress max="3" class="safe-line" value="2">
              </progress>
            </div>
          </div>
          <div class="item flex-view">
            <div class="label">{{ lang.bindphone[this.$store.state.language] }}</div>
            <div class="right-box">
              <input class="input-dom" :placeholder=lang.plsenterphone[this.$store.state.language]>
              <a-button type="link" @click="handleBindMobile()">{{ lang.change[this.$store.state.language] }}</a-button>
            </div>
          </div>
        </div>
        <div class="edit-pwd-box" style="display;">
          <div class="pwd-edit">
            <!---->
            <div class="item flex-view">
              <div class="label">{{ lang.nowpwd[this.$store.state.language] }}</div>
              <div class="right-box">
                <a-input-password :placeholder=lang.plsenternowpwd[this.$store.state.language] v-model="password" />
              </div>
            </div>
            <div class="item flex-view">
              <div class="label">{{ lang.newpwd[this.$store.state.language] }}</div>
              <div class="right-box">
                <a-input-password :placeholder=lang.enternewpwd[this.$store.state.language] v-model="newPassword1" />
              </div>
            </div>
            <div class="item flex-view">
              <div class="label">{{ lang.surenewpwd[this.$store.state.language] }}</div>
              <div class="right-box">
                <a-input-password :placeholder=lang.againenterpwd[this.$store.state.language] v-model="newPassword2" />
              </div>
            </div>
            <div class="item flex-view">
              <div class="label">
              </div>
              <div class="right-box">
                <a-button type="primary" @click="handleUpdatePwd()">{{ lang.changepwd[this.$store.state.language] }}</a-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {updatePwdApi} from '@/api/index/user'
import langData from '@/lang/lang.json'

export default  {
  name: 'SecurityView',
  data () {
    return {
      password: undefined,
      newPassword1: undefined,
      newPassword2: undefined,
      lang: langData
    }
  },
  mounted () {
    this.locale()
  },
  methods: {
    locale () {
      return this.$store.state.language;
    },
    handleBindMobile () {
      if (this.$store.state.language === 'zh') {
        this.$message.info('功能开发中')
      } else {
        this.$message.info('In function development')
      }
    },
    handleUpdatePwd () {
      if (!this.password || !this.newPassword1 || !this.newPassword2) {
        if (this.$store.state.language === 'zh') {
          this.$message.warn('不能为空')
        } else {
          this.$message.warn('can not be empty')
        }
        return
      }
      if (this.newPassword1 !== this.newPassword2) {
        if (this.$store.state.language === 'zh') {
          this.$message.warn('密码不一致')
        } else {
          this.$message.warn('Password inconsistency')
        }
        return
      }

      let id = this.$store.state.user.userId
      updatePwdApi({id: id}, {
        password: this.password,
        newPassword1: this.newPassword1,
        newPassword2: this.newPassword2
      }).then(res => {
        if (this.$store.state.language === 'zh') {
          this.$message.success('修改成功')
        } else {
          this.$message.success('change success')
        }
      }).catch(err => {
        this.$message.error(err.msg)
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

.safe-view {
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

    .flex-center {
      -webkit-box-align: center;
      -ms-flex-align: center;
      align-items: center;
    }

    .safe-text {
      color: #f62a2a;
      font-weight: 600;
      font-size: 14px;
      margin-right: 18px;
    }

    .safe-line {
      background: #d3dce6;
      border-radius: 8px;
      width: 280px;
      height: 8px;
      overflow: hidden;
      color: #f6982a;
    }

    .input-dom {
      background: #f8fafb;
      border-radius: 4px;
      width: 240px;
      height: 40px;
      line-height: 40px;
      font-size: 14px;
      color: #5f77a6;
      padding: 0 12px;
      margin-right: 16px;
    }

    .change-btn {
      color: #4684e2;
      font-size: 14px;
      border: none;
      outline: none;
      cursor: pointer;
    }

    .wx-text {
      color: #5f77a6;
      font-size: 14px;
      margin-right: 16px;
    }

    .edit-pwd-btn {
      color: #4684e2;
      font-size: 14px;
      cursor: pointer;
    }
  }
}
</style>
