<template>
  <a-form-model
    ref="myform"
    :model="form"
    :rules="rules">
    <a-row :gutter="24">
      <a-col span="24">
        <a-form-model-item :label=lang.bannerpicture[this.$store.state.language]>
          <a-upload-dragger
            name="file"
            accept="image/*"
            :multiple="false"
            :before-upload="beforeUpload"
          >
            <p class="ant-upload-drag-icon">
              <template v-if="imageUrl">
                <img :src="imageUrl"  style="width: 60px;height: 40px;"/>
              </template>
              <template v-else>
                <a-icon type="inbox" />
              </template>
            </p>
            <p class="ant-upload-text">
              {{ lang.plsselectpicture[this.$store.state.language] }}
            </p>
          </a-upload-dragger>
        </a-form-model-item>
      </a-col>
      <a-col span="24">
        <a-form-model-item :label=lang.link[this.$store.state.language] prop="link">
          <a-input :placeholder=lang.plsenter[this.$store.state.language] v-model="form.link"/>
        </a-form-model-item>
      </a-col>
    </a-row>
  </a-form-model>
</template>

<script>
import {createApi, updateApi} from '@/api/admin/ad'
import langData from '@/lang/lang.json'

export default {
  name: 'EditAd',
  props: {
    modifyFlag: {
      type: Boolean,
      default: () => false
    },
    ad: {
      type: Object,
      default: () => {}
    }
  },
  data () {
    return {
      imageUrl: undefined,
      lang: langData,
      form: {
      },
      rules: {
        link: [{ required: true, message: '请输入链接', trigger: 'change' }]
      }
    }
  },
  created () {
    if (this.modifyFlag) {
      this.form = this.ad
      this.imageUrl = this.ad.image
      this.form.image = undefined
    }
  },
  mounted () {
    this.locale()
  },
  methods: {
    locale () {
      return this.$store.state.language;
    },
    beforeUpload (file) {
      // 改文件名
      const fileName = new Date().getTime().toString() + '.' + file.type.substring(6)
      const copyFile = new File([file], fileName)
      console.log(copyFile)
      this.form.image = copyFile
      return false
    },
    onOk () {
      return new Promise((resolve, reject) => {
        console.log(this.form)
        const formData = new FormData()
        if (this.form.image) {
          formData.append('image', this.form.image)
        }
        if (this.form.link) {
          formData.append('link', this.form.link)
        }
        this.$refs.myform.validate(valid => {
          if (valid) {
            if (this.modifyFlag) {
              // 修改接口
              updateApi({
                id: this.ad.id
              }, formData).then(res => {
                console.log(res)
                resolve(true)
              }).catch(err => {
                this.$message.error(err.msg || '更新失败')
                reject(new Error('更新失败'))
              })
            } else {
              // 新增接口
              createApi(formData).then(res => {
                console.log(res)
                resolve(true)
              }).catch(err => {
                this.$message.error(err.msg || '新建失败')
                reject(new Error('新建失败'))
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
