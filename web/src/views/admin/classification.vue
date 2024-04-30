<template>
  <div class="page-view">
    <div class="table-operation">
      <a-space>
        <a-button type="primary" @click="handleAdd(-1)">{{ lang.add[this.$store.state.language] }}</a-button>
        <a-button @click="handleBatchDelete">{{ lang.mutdel[this.$store.state.language] }}</a-button>
      </a-space>
    </div>
    <div v-if="this.$store.state.language === 'zh'" class="table-wrap" ref="tableWrap">
      <a-table
        size="middle"
        rowKey="key"
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
        <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a v-if="record.isParent" @click="handleAdd(record.key)">新增</a>
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
        rowKey="key"
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
        <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a v-if="record.isParent" @click="handleAdd(record.key)">Add</a>
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
import {listApi, deleteApi} from '@/api/admin/classification'
import EditClassification from '@/views/admin/model/edit-classification'
import langData from '@/lang/lang.json'
import en_US from "ant-design-vue/lib/locale/en_US";

const columns = [
  {
    title: '分类名称',
    dataIndex: 'title',
    key: 'title',
  },
  {
    title: '英文分类名称',
    dataIndex: 'en_title',
    key: 'title',
  },
  {
    title: '操作',
    dataIndex: 'action',
    align: 'right',
    fixed: 'right',
    width: 140,
    scopedSlots: { customRender: 'operation' }
  }
]
const encolumns = [
  {
    title: 'Title',
    dataIndex: 'title',
    key: 'title',
  },
  {
    title: 'En Title',
    dataIndex: 'en_title',
    key: 'title',
  },
  {
    title: 'Operate',
    dataIndex: 'action',
    align: 'right',
    fixed: 'right',
    width: 140,
    scopedSlots: { customRender: 'operation' }
  }
]

export default {
  name: 'Classification',
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
        this.data = res.data
      })
    },
    rowSelection () {
      return {
        onChange: (selectedRowKeys, selectedRows) => {
          for (let i=0; i<selectedRows.length; i++) {
            console.log(333, selectedRows[i].id)
            this.selectedRowKeys.push(selectedRows[i].id)
          }
          this.selectedRowKeys = Array.from(new Set(this.selectedRowKeys));
        },
        onSelect: (record, selected, selectedRows) => {
          console.log(record, selected, selectedRows);
        },
      }
    },
    handleAdd (pid) {
      if (this.$store.state.language === 'zh') {
        this.$dialog(
        EditClassification,
        {
          pid: pid,
          on: {
            ok: () => {
              this.page = 1
              this.getList()
            }
          }
        },
        {
          title: '新增分类',
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
        EditClassification,
        {
          pid: pid,
          on: {
            ok: () => {
              this.page = 1
              this.getList()
            }
          }
        },
        {
          title: 'Add Classification',
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
        EditClassification,
        {
          classification: Object.assign({}, record),
          modifyFlag: true,
          on: {
            ok: () => {
              this.getList()
            }
          }
        },
        {
          title: '编辑分类',
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
        EditClassification,
        {
          classification: Object.assign({}, record),
          modifyFlag: true,
          on: {
            ok: () => {
              this.getList()
            }
          }
        },
        {
          title: 'Edit Classification',
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
      if (this.$store.state.language === 'zh') {
        const that = this
        this.$confirm({
        title: '确定删除?',
        content: '该分类下的商品也会被删除！',
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
        content: 'The goods under this category will also be deleted！',
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
      console.log(this.selectedRowKeys.id)
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
        content: '该分类下的商品也会被删除！',
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
        content: 'The goods under this category will also be deleted！',
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
            that.$message.error(err.msg || 'delte failed')
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
