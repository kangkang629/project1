<template>
  <a-form-model v-if="this.$store.state.language === 'zh'"
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="姓名" prop="name">
          <a-input placeholder="请输入" v-model="form.name"></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="电话号码" prop="mobile">
          <a-input placeholder="请输入" v-model="form.mobile"></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="送货地址" prop="desc">
          <a-input placeholder="请输入" v-model="form.desc"></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="默认地址">
          <a-switch v-model="form.default"></a-switch>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
  <a-form-model v-else-if="this.$store.state.language === 'en'"
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="Name" prop="name">
          <a-input placeholder="Please enter" v-model="form.name"></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="Phone" prop="mobile">
          <a-input placeholder="Please enter" v-model="form.mobile"></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="Address" prop="desc">
          <a-input placeholder="Please enter" v-model="form.desc"></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item label="Default Address">
          <a-switch v-model="form.default"></a-switch>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {createApi, updateApi} from '@/api/index/address'
import langData from '@/lang/lang.json'

export default {
  name: 'EditAddress',
  props: {
    modifyFlag: {
      type: Boolean,
      default: () => false
    },
    address: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      form: {
        name: undefined,
        mobile: undefined,
        desc: undefined,
        default: undefined,
        lang: langData
      }
    }
  },
  created () {
    if (this.modifyFlag) {
      this.form = this.address
    }
  },
  mounted () {
    this.locale()
  },
  methods: {
    locale () {
      return this.$store.state.language;
    },
    onOk () {
      return new Promise((resolve, reject) => {
        console.log(this.form)
        const formData = new FormData()
        formData.append('user', this.$store.state.user.userId)
        formData.append('default', this.form.default ? this.form.default : false)
        if (this.form.name) {
          formData.append('name', this.form.name)
        }
        if (this.form.mobile) {
          formData.append('mobile', this.form.mobile)
        }
        if (this.form.desc) {
          formData.append('desc', this.form.desc)
        }
        this.$refs.myform.validate(valid => {
          if (valid) {
            if (this.modifyFlag) {
              // 修改接口
              updateApi({
                id: this.address.id
              }, formData).then(res => {
                console.log(res)
                resolve(true)
              }).catch(err => {
                if ( this.$store.state.language === 'zh') {
                  this.$message.error(err.msg || '更新失败')
                  reject(new Error('更新失败'))
                } else {
                  this.$message.error(err.msg || 'Update failed')
                  reject(new Error('Update failed'))
                }

              })
            } else {
              // 新增接口
              createApi(formData).then(res => {
                console.log(res)
                resolve(true)
              }).catch(err => {
                if ( this.$store.state.language === 'zh') {
                  this.$message.error(err.msg || '新建失败')
                  reject(new Error('新建失败'))
                } else {
                  this.$message.error(err.msg || 'Add failed')
                  reject(new Error('Add failed'))
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
