<template>
  <a-form-model
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row v-if="this.$store.state.language === 'zh'" :gutter="24">
      <a-col span="24">
        <a-form-model-item label="用户名" prop="username">
          <a-input :disabled="modifyFlag" placeholder="请输入" v-model="form.username" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24" v-if="!modifyFlag">
        <a-form-model-item label="密码" prop="password">
          <a-input placeholder="请输入" type="password" v-model="form.password" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="昵称" prop="nickname">
          <a-input placeholder="请输入" v-model="form.nickname" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="角色" prop="role">
          <a-select placeholder="请选择" allowClear v-model="form.role">
            <template v-for="item in roleData">
              <a-select-option :key="item.id" :value="item.id">{{ item.title }}</a-select-option>
            </template>
          </a-select>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="状态" prop="status">
          <a-select placeholder="请选择" allowClear v-model="form.status">
            <a-select-option key="0" value="0">正常</a-select-option>
            <a-select-option key="1" value="1">封号</a-select-option>
          </a-select>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="邮箱" prop="email">
          <a-input placeholder="请输入" v-model="form.email" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="手机号" prop="mobile">
          <a-input placeholder="请输入" v-model="form.mobile" allowClear></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
    <a-row v-if="this.$store.state.language === 'en'" :gutter="24">
      <a-col span="24">
        <a-form-model-item label="username" prop="username">
          <a-input :disabled="modifyFlag" placeholder="please enter" v-model="form.username" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24" v-if="!modifyFlag">
        <a-form-model-item label="password" prop="password">
          <a-input placeholder="please enter" type="password" v-model="form.password" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="nickname" prop="nickname">
          <a-input placeholder="please enter" v-model="form.nickname" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="role" prop="role">
          <a-select placeholder="please select" allowClear v-model="form.role">
            <template v-for="item in enroleData">
              <a-select-option :key="item.id" :value="item.id">{{ item.title }}</a-select-option>
            </template>
          </a-select>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="status" prop="status">
          <a-select placeholder="please select" allowClear v-model="form.status">
            <a-select-option key="0" value="0">Normal</a-select-option>
            <a-select-option key="1" value="1">Ban</a-select-option>
          </a-select>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="email" prop="email">
          <a-input placeholder="please enter" v-model="form.email" allowClear></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="mobile" prop="mobile">
          <a-input placeholder="please enter" v-model="form.mobile" allowClear></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {createApi, updateApi} from '@/api/admin/user'
import langData from '@/lang/lang.json'

const RoleData = [
  {
    id: '1',
    title: '管理员'
  },
  {
    id: '2',
    title: '普通用户'
  },
  {
    id: '3',
    title: '演示帐号'
  }
]
const enRoleData = [
  {
    id: '1',
    title: 'administrators'
  },
  {
    id: '2',
    title: 'Ordinary users'
  },
  {
    id: '3',
    title: 'Demo account'
  }
]
export default {
  name: 'EditUser',
  props: {
    modifyFlag: {
      type: Boolean,
      default: () => false
    },
    user: {
      type: Object,
      default: () => {
      }
    }
  },
  data () {
    return {
      roleData: RoleData,
      enroleData: enRoleData,
      form: {
        username: undefined,
        role: undefined,
        nickname: undefined,
        email: undefined,
        mobile: undefined,
        lang: langData
      },
      rules: {
        username: [{required: true, message: '请输入用户名', trigger: 'change'}],
        password: [{required: true, message: '请输入密码', trigger: 'change'}],
        role: [{required: true, message: '请选择角色', trigger: 'change'}],
        status: [{required: true, message: '请选择状态', trigger: 'change'}]
      }
    }
  },
  created () {
    if (this.modifyFlag) {
      console.log(this.user)
      for (const key in this.user) {
        if (this.user[key]) {
          this.form[key] = this.user[key]
        }
      }
    }
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
            if (this.modifyFlag) {
              // 修改接口
              if (this.form.avatar) {
                // 头像不修改
                delete this.form['avatar']
              }
              updateApi({
                id: this.user.id
              }, this.form).then(res => {
                console.log(res)
                resolve(true)
              }).catch(err => {
                if (this.$store.state.language === 'zh') {
                  this.$message.error(err.msg || '更新失败')
                  reject(new Error('更新失败'))
                } else {
                  this.$message.error(err.msg || 'update failed')
                  reject(new Error('update failed'))
                }
              })
            } else {
              // 新增接口
              createApi(this.form).then(res => {
                console.log(res)
                resolve(true)
              }).catch(err => {
                if (this.$store.state.language === 'zh') {
                  this.$message.error(err.msg || '新建失败')
                  reject(new Error('新建失败'))
                } else {
                  this.$message.error(err.msg || 'add failed')
                  reject(new Error('add failed'))
                }
              })
            }
          }
        })
      })
    }
  }
}
</script>

<style lang="less" scoped>

</style>
