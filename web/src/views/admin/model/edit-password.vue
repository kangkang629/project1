<template>
  <a-form-model
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row v-if="this.$store.state.language === 'zh'" :gutter="24">
      <a-col span="24">
        <a-form-model-item label="原密码" prop="password">
          <a-input :placeholder="请输入" type="password" v-model="form.password" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="新密码" prop="newPassword1">
          <a-input placeholder="请输入" type="password" v-model="form.newPassword1" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="确认新密码" prop="newPassword2">
          <a-input placeholder="请输入" type="password" v-model="form.newPassword2" allowClear></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
    <a-row v-if="this.$store.state.language === 'en'" :gutter="24">
      <a-col span="24">
        <a-form-model-item label="Original password" prop="password">
          <a-input placeholder="Please Enter" type="password" v-model="form.password" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="New password" prop="newPassword1">
          <a-input placeholder="Please Enter" type="password" v-model="form.newPassword1" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="Confirm password" prop="newPassword2">
          <a-input placeholder="Please Enter" type="password" v-model="form.newPassword2" allowClear></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {updatePwdApi} from '@/api/admin/user'
import langData from '@/lang/lang.json'

export default {
  name: 'EditPassword',
  props: {
    user: {
      type: Object,
      default: () => {
      }
    }
  },
  data () {
    return {
      form: {
        password: undefined,
        newPassword1: undefined,
        newPassword2: undefined,
        lang: langData
      },
      rules: {
        password: [{required: true, message: '请输入密码', trigger: 'change'}],
        newPassword1: [{required: true, message: '请输入新密码', trigger: 'change'}],
        newPassword2: [{required: true, message: '请输入确认密码', trigger: 'change'}]
      }
    }
  },
  created () {
  },
  mounted () {
    locale ()
  },
  methods: {
    locale () {
      return this.$store.state.language;
    },
    onOk () {
      return new Promise((resolve, reject) => {
        console.log(this.form)
        this.$refs.myform.validate(valid => {
          if (valid) {
            // 修改接口
            updatePwdApi({
              id: this.user.id
            }, this.form).then(res => {
              console.log(res)
              resolve(true)
            }).catch(err => {
              this.$message.error(err.msg || '更新失败')
              reject(new Error('更新失败'))
            })
          }
        })
      })
    }
  }
}
</script>

<style lang="less" scoped>

</style>
