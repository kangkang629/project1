<template>
  <div class="page-view">
      <div class="table-operation">
        <a-space>
          <a-button type="primary" @click="handleAdd">{{ lang.add[this.$store.state.language] }}</a-button>
          <a-button @click="handleBatchDelete">{{ lang.mutdel[this.$store.state.language] }}</a-button>
        </a-space>
      </div>
      <div v-if="this.$store.state.language === 'zh'" class="table-wrap" ref="tableWrap">
        <a-table
          size="middle"
          rowKey="id"
          bordered
          :loading="loading"
          :columns="columns"
          :data-source="data"
          :scroll="{ x: 'max-content' }"
          :row-selection="rowSelection()"
          :pagination="{
          size: 'default',
          current: page,
          pageSize: pageSize,
          onChange: (current) => page = current,
          pageSizeOptions: ['10', '20', '30', '40'],
          showSizeChanger: true,
          showTotal: (total) => `共${total}条数据`
        }"
        >
          <template slot="image" slot-scope="text" >
            <img :src="text" style="width: 60px;height: 40px;"/>
          </template>
          <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a @click="handleEdit(record)">编辑</a>
            <a @click="handleDelete(record)">删除</a>
          </a-space>
        </span>
        </a-table>
      </div>
          <div v-if="this.$store.state.language === 'en'" class="table-wrap" ref="tableWrap">
            <a-config-provider :locale="en_US">
        <a-table
          size="middle"
          rowKey="id"
          bordered
          :loading="loading"
          :columns="enColumns"
          :data-source="data"
          :scroll="{ x: 'max-content' }"
          :row-selection="rowSelection()"
          :pagination="{
          size: 'default',
          current: page,
          pageSize: pageSize,
          onChange: (current) => page = current,
          pageSizeOptions: ['10', '20', '30', '40'],
          showSizeChanger: true,
          showTotal: (total) => `${total} pieces of data in total`
        }"
        >
          <template slot="image" slot-scope="text" >
            <img :src="text" style="width: 60px;height: 40px;"/>
          </template>
          <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a @click="handleEdit(record)">Edit</a>
            <a @click="handleDelete(record)">Delete</a>
          </a-space>
        </span>
        </a-table>
              </a-config-provider>
      </div>
    </div>
</template>

<script>
import {listApi, deleteApi} from '@/api/admin/ad'
import EditAd from '@/views/admin/model/edit-ad'
import langData from '@/lang/lang.json'
import en_US from "ant-design-vue/lib/locale/en_US";

const enColumns = [
  {
    title: 'No',
    dataIndex: 'index',
    key: 'index',
    align: 'center'
  },
  {
    title: 'Picture',
    dataIndex: 'image',
    key: 'image',
    align: 'center',
    scopedSlots: { customRender: 'image' }
  },
  {
    title: 'Link',
    dataIndex: 'link',
    key: 'link',
    align: 'center'
  },
  {
    title: 'Operate',
    dataIndex: 'action',
    align: 'center',
    fixed: 'right',
    width: 140,
    scopedSlots: { customRender: 'operation' }
  }
]


const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    align: 'center'
  },
  {
    title: '图片',
    dataIndex: 'image',
    key: 'image',
    align: 'center',
    scopedSlots: { customRender: 'image' }
  },
  {
    title: '跳转链接',
    dataIndex: 'link',
    key: 'link',
    align: 'center'
  },
  {
    title: '操作',
    dataIndex: 'action',
    align: 'center',
    fixed: 'right',
    width: 140,
    scopedSlots: { customRender: 'operation' }
  }
]

export default {
  name: 'Ad',
  computed: {
    en_US() {
      return en_US
    }
  },
  data () {
    return {
      loading: false,
      selectedRowKeys: [],
      columns,
      enColumns,
      data: [],
      pageSize: 10,
      page: 1,
      lang: langData
    }
  },
  methods: {
    locale () {
      return this.$store.state.language;
    },
    getList () {
      this.loading = true
      listApi().then(res => {
        this.loading = false
        res.data.forEach((item, index) => {
          item.index = index + 1
          if (item.image) {
            item.image = this.$BASE_URL + item.image
          }
        })
        this.data = res.data
        console.log(res)
      })
    },
    rowSelection () {
      return {
        onChange: (selectedRowKeys, selectedRows) => {
          this.selectedRowKeys = selectedRowKeys
        }
      }
    },
    handleAdd () {
      if (this.$store.state.language === 'zh') {
              this.$dialog(
        EditAd,
        {
          on: {
            ok: () => {
              this.page = 1
              this.getList()
            }
          }
        },
        {
          title: '新增广告',
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
        EditAd,
        {
          on: {
            ok: () => {
              this.page = 1
              this.getList()
            }
          }
        },
        {
          title: 'Add Ad',
          cancelText: 'Cancel',
          okText: 'Ok',
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
    handleEdit (record) {
      if (this.$store.state.language === 'zh') {
              this.$dialog(
        EditAd,
        {
          ad: Object.assign({}, record),
          modifyFlag: true,
          on: {
            ok: () => {
              this.getList()
            }
          }
        },
        {
          title: '编辑广告',
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
        EditAd,
        {
          ad: Object.assign({}, record),
          modifyFlag: true,
          on: {
            ok: () => {
              this.getList()
            }
          }
        },
        {
          title: 'Edit AD',
          cancelText: 'Cancel',
          okText: 'Ok',
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
    // 删除
    handleDelete (record) {
      const that = this
      if (this.$store.state.language === 'zh') {
        this.$confirm({
        title: '确定删除?',
        onOk () {
          deleteApi({
            ids: record.id
          }).then(res => {
            that.$message.success('删除成功')
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || '删除失败')
          })
        }
      })
      } else {
        this.$confirm({
        title: 'delete confirm?',
        cancelText: 'Cancel',
        okText: 'Ok',
        onOk () {
          deleteApi({
            ids: record.id
          }).then(res => {
            that.$message.success('delete success')
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || 'delete failed')
          })
        }
      })
      }

    },
    // 批量删除
    handleBatchDelete () {
      console.log(this.selectedRowKeys)
      if (this.selectedRowKeys.length <= 0) {
        if (this.$store.state.language === 'zh') {
            this.$message.warn('请勾选删除项')
            return
        } else {
            this.$message.warn('Please check the delete option')
            return
        }
      }
      const that = this
      if (this.$store.state.language === 'zh') {
        this.$confirm({
        title: '确定删除?',
        onOk () {
          deleteApi({
            ids: that.selectedRowKeys.join(',')
          }).then(res => {
            that.$message.success('删除成功')
            that.selectedRowKeys = []
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || '删除失败')
          })
        }
      })
      } else {
        this.$confirm({
        title: 'delete confirm?',
        onOk () {
          deleteApi({
            ids: that.selectedRowKeys.join(',')
          }).then(res => {
            that.$message.success('delete success')
            that.selectedRowKeys = []
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || 'delete failed')
          })
        }
      })
      }
    }
  },
  mounted () {
    this.getList()
    this.locale()
  }
}
</script>

<style lang="less" scoped>
.table-wrap {
  flex: 1;
}
.page-view {
  min-height: 100%;
  background: #FFF;
  padding: 24px;
  display: flex;
  flex-direction: column;
}
.table-operation {
  height: 50px;
  text-align: right;
}
</style>
