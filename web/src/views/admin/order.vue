<template>
  <div class="page-view">
    <div class="table-operation">
      <a-space>
<!--        <a-button type="primary" @click="handleMockAdd">模拟新增</a-button>-->
        <a-button @click="handleBatchDelete">{{ lang.mutdel[this.$store.state.language] }}</a-button>
      </a-space>
    </div>
    <div v-if="this.$store.state.language === 'zh'" class="table-wrap" ref="tableWrap">
      <a-table
        size="middle"
        rowKey="id"
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
        <span slot="status" slot-scope="text">
          <a-tag :color="text === '1'? '#2db7f5':'#87d068'">
            {{text === '1'? '待支付': text === '2'? '已支付':'已取消'}}
          </a-tag>
        </span>
        <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a @click="handleCancel(record)">取消</a>
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
        :loading="loading"
        :columns="encolumns"
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
        <span slot="status" slot-scope="text">
          <a-tag :color="text === '1'? '#2db7f5':'#87d068'">
            {{text === '1'? 'Unpaid': text === '2'? 'Paid':'Cancel'}}
          </a-tag>
        </span>
        <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a @click="handleCancel(record)">Cancel</a>
            <a @click="handleDelete(record)">Delete</a>
          </a-space>
        </span>
      </a-table>
      </a-config-provider>
    </div>
  </div>
</template>

<script>
import {listApi, createApi, updateApi, cancelOrderApi, delayApi, deleteApi} from '@/api/admin/order'
import langData from '@/lang/lang.json'
import en_US from "ant-design-vue/lib/locale/en_US";

const columns = [
  {
    title: '序号',
    dataIndex: 'index',
    key: 'index',
    align: 'center'
  },
  {
    title: '用户',
    dataIndex: 'username',
    key: 'username',
    align: 'center'
  },
  {
    title: '商品',
    dataIndex: 'title',
    key: 'title',
    align: 'center',
    customRender: (text) => text ? text.substring(0, 10) + '...' : '--'
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    align: 'center',
    scopedSlots: {customRender: 'status'}
  },
  {
    title: '订单时间',
    dataIndex: 'order_time',
    key: 'order_time',
    align: 'center'
  },
  {
    title: '期望送达时间',
    dataIndex: 'delivery_time',
    key: 'delivery_time',
    align: 'center'
  },
  {
    title: '操作',
    dataIndex: 'action',
    align: 'center',
    fixed: 'right',
    width: 140,
    scopedSlots: {customRender: 'operation'}
  }
]
const encolumns = [
  {
    title: 'No',
    dataIndex: 'index',
    key: 'index',
    align: 'center'
  },
  {
    title: 'User',
    dataIndex: 'username',
    key: 'username',
    align: 'center'
  },
  {
    title: 'Goods',
    dataIndex: 'title',
    key: 'title',
    align: 'center',
    customRender: (text) => text ? text.substring(0, 10) + '...' : '--'
  },
  {
    title: 'Status',
    dataIndex: 'status',
    key: 'status',
    align: 'center',
    scopedSlots: {customRender: 'status'}
  },
  {
    title: 'Order Time',
    dataIndex: 'order_time',
    key: 'order_time',
    align: 'center'
  },
  {
    title: 'Delivery Time',
    dataIndex: 'delivery_time',
    key: 'delivery_time',
    align: 'center'
  },
  {
    title: 'Operate',
    dataIndex: 'action',
    align: 'center',
    fixed: 'right',
    width: 140,
    scopedSlots: {customRender: 'operation'}
  }
]

export default {
  name: 'Order',
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
      encolumns,
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
    handleMockAdd () {
      createApi({
        thing: 1,
        user: 2,
        count: 1
      }).then(res => {
        this.getList()
      }).catch(err => {

      })
    },
    // 取消
    handleCancel (record) {
      if (this.$store.state.language === 'zh') {
        const that = this
        this.$confirm({
        title: '确定取消?',
        onOk () {
          cancelOrderApi({
            id: record.id
          }).then(res => {
            that.$message.success('取消成功')
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || '取消失败')
          })
        }
      })
      } else {
        const that = this
        this.$confirm({
        title: 'delete confirm?',
        cancelText: 'Cancel',
        okText: 'Ok',
        onOk () {
          cancelOrderApi({
            id: record.id
          }).then(res => {
            that.$message.success('cancel success')
            that.getList()
          }).catch(err => {
            that.$message.error(err.msg || 'cancel failed')
          })
        }
      })
      }

    },
    // 删除
    handleDelete (record) {
      if (this.$store.state.language === 'zh') {
        const that = this
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
        const that = this
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
        } else {
          this.$message.warn('Please check the delete option')
        }
        return
      }
      if (this.$store.state.language === 'zh') {
        const that = this
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
        const that = this
        this.$confirm({
        title: 'delete confirm?',
        cancelText: 'Cancel',
        okText: 'Ok',
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
    locale ()
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
