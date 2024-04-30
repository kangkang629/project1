<template>
  <a-form-model
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item :label=lang.title[this.$store.state.language] prop="title">
          <a-input :placeholder=lang.plsentertitle[this.$store.state.language] v-model="form.title"></a-input>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item :label=lang.noticecontent[this.$store.state.language] prop="content">
          <a-textarea :placeholder=lang.plsentercontent[this.$store.state.language] :rows="4" v-model="form.content"></a-textarea>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {createApi, updateApi} from '@/api/admin/notice'
import langData from '@/lang/lang.json'

export default {
  name: 'EditNotice',
  props: {
    modifyFlag: {
      type: Boolean,
      default: () => false
    },
    notice: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      form: {
      },
      lang: langData,
      rules: {
        title: [{ required: true, message: '请输入通知标题', trigger: 'change' }],
        content: [{ required: true, message: '请输入通知内容', trigger: 'change' }],
      }
    }
  },
  created () {
    if (this.modifyFlag) {
      this.form = this.notice
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
        const formData = new FormData()
        if (this.form.content) {
          formData.append('content', this.form.content)
        }
        if (this.form.title) {
          formData.append('title', this.form.title)
        }
        this.$refs.myform.validate(valid => {
          if (valid) {
            if (this.modifyFlag) {
              // 修改接口
              updateApi({
                id: this.notice.id
              }, formData).then(res => {
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
              createApi(formData).then(res => {
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
