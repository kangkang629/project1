<template>
  <a-form-model
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row v-if="this.$store.state.language === 'zh'" :gutter="24">
      <a-col span="24">
        <a-form-model-item label="分类名称" prop="title">
          <a-input placeholder="请输入" v-model="form.title"></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="分类名称(英文)" prop="en_title">
          <a-input placeholder="请输入" v-model="form.en_title"></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
    <a-row v-if="this.$store.state.language === 'en'" :gutter="24">
      <a-col span="24">
        <a-form-model-item label="classification name" prop="title">
          <a-input placeholder="please enter" v-model="form.title"></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item label="classification name(en)" prop="en_title">
          <a-input placeholder="please enter" v-model="form.en_title"></a-input>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {createApi, updateApi} from '@/api/admin/classification'
import langData from '@/lang/lang.json'

export default {
  name: 'EditClassification',
  props: {
    modifyFlag: {
      type: Boolean,
      default: () => false
    },
    pid: {
      type: Number,
      default: () => -1
    },
    classification: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      form: {
        title: undefined,
        en_title: undefined
      },
      rules: {
        title: [{ required: true, message: '请输入分类名称', trigger: 'change' }]
      },
      lang: langData
    }
  },
  created () {
    if (this.modifyFlag) {
      this.form.en_title = this.classification.en_title
      this.form.title = this.classification.title
      this.form.id = this.classification.id
    }
    if (this.pid > 0) {
      this.form.pid = this.pid
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
        this.$refs.myform.validate(valid => {
          if (valid) {
            if (this.modifyFlag) {
              // 修改接口
              updateApi({
                id: this.form.id
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
                this.$message.error(err.msg || 'add failed')
                reject(new Error('add failed'))
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
