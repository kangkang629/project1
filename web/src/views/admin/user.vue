<template>
  <div class="page-view">
    <div class="table-operation">
      <a-space>
        <a-button type="primary" @click="handleAdd">{{  lang.add[this.$store.state.language] }}</a-button>
        <a-button @click="handleBatchDelete">{{  lang.mutdel[this.$store.state.language] }}</a-button>
        <a-input-search :addon-before=lang.username[this.$store.state.language] enter-button @search="onSearch" @change="onSearchChange" />
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
        <span slot="role" slot-scope="text">
          <span v-if="text === '1'">管理员</span>
          <span v-if="text === '2'">普通用户</span>
          <span v-if="text === '3'">演示帐号</span>
        </span>
        <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a @click="handleEdit(record)">编辑</a>
            <a @click="handleUpdatePwd(record)" :disabled="record.username !== currentAdminUserName">改密</a>
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
        <span slot="role" slot-scope="text">
          <span v-if="text === '1'">administrators</span>
          <span v-if="text === '2'">Ordinary users</span>
          <span v-if="text === '3'">Demo account</span>
        </span>
        <span slot="operation" class="operation" slot-scope="text, record">
          <a-space :size="16">
            <a @click="handleEdit(record)">Edit</a>
            <a @click="handleUpdatePwd(record)" :disabled="record.username !== currentAdminUserName">Change Password</a>
            <a @click="handleDelete(record)">Delete</a>
          </a-space>
        </span>
      </a-table>
      </a-config-provider>
    </div>
  </div>
</template>

<script>
import {listApi, deleteApi} from '@/api/admin/user'
import EditUser from '@/views/admin/model/edit-user'
import EditPassword from '@/views/admin/model/edit-password'
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
    title: '用户名',
    dataIndex: 'username',
    key: 'username',
    align: 'center'
  },
  {
    title: '昵称',
    dataIndex: 'nickname',
    key: 'nickname',
    align: 'center'
  },
  {
    title: '角色',
    dataIndex: 'role',
    key: 'role',
    align: 'center',
    scopedSlots: { customRender: 'role' }
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    align: 'center',
    customRender: (text) => text === '0' ? '正常' : '封号'
  },
  {
    title: '邮箱',
    dataIndex: 'email',
    key: 'email',
    align: 'center'
  },
  {
    title: '手机号',
    dataIndex: 'mobile',
    key: 'mobile',
    align: 'center'
  },
  {
    title: '创建时间',
    dataIndex: 'create_time',
    key: 'create_time',
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
const encolumns = [
  {
    title: 'No',
    dataIndex: 'index',
    key: 'index',
    align: 'center'
  },
  {
    title: 'Username',
    dataIndex: 'username',
    key: 'username',
    align: 'center'
  },
  {
    title: 'Nickname',
    dataIndex: 'nickname',
    key: 'nickname',
    align: 'center'
  },
  {
    title: 'Role',
    dataIndex: 'role',
    key: 'role',
    align: 'center',
    scopedSlots: { customRender: 'role' }
  },
  {
    title: 'Status',
    dataIndex: 'status',
    key: 'status',
    align: 'center',
    customRender: (text) => text === '0' ? 'Normal' : 'Ban'
  },
  {
    title: 'Email',
    dataIndex: 'email',
    key: 'email',
    align: 'center'
  },
  {
    title: 'Mobile',
    dataIndex: 'mobile',
    key: 'mobile',
    align: 'center'
  },
  {
    title: 'Create Time',
    dataIndex: 'create_time',
    key: 'create_time',
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

export default {
  name: 'User',
  computed: {
    en_US() {
      return en_US
    }
  },
  data () {
    return {
      loading: false,
      currentAdminUserName: '',
      keyword: '',
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
      listApi({
        keyword: this.keyword
      }).then(res => {
        this.loading = false
        res.data.forEach((item, index) => {
          item.index = index + 1
        })
        this.data = res.data
        console.log(res)
      })
    },
    onSearchChange (e) {
      this.keyword = e.target.value
    },
    onSearch (value) {
      this.getList()
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
        EditUser,
        {
          on: {
            ok: () => {
              this.page = 1
              this.getList()
            }
          }
        },
        {
          title: '新增用户',
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
        EditUser,
        {
          on: {
            ok: () => {
              this.page = 1
              this.getList()
            }
          }
        },
        {
          title: 'Add User',
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
    handleUpdatePwd (record) {
      if (this.$store.state.language === 'zh') {
              this.$dialog(
        EditPassword,
        {
          user: Object.assign({}, record),
          on: {
            ok: () => {
              this.getList()
            }
          }
        },
        {
          title: '修改密码',
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
        EditPassword,
        {
          user: Object.assign({}, record),
          on: {
            ok: () => {
              this.getList()
            }
          }
        },
        {
          title: 'Change Password',
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
        EditUser,
        {
          user: Object.assign({}, record),
          modifyFlag: true,
          on: {
            ok: () => {
              this.getList()
            }
          }
        },
        {
          title: '编辑用户',
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
        EditUser,
        {
          user: Object.assign({}, record),
          modifyFlag: true,
          on: {
            ok: () => {
              this.getList()
            }
          }
        },
        {
          title: 'Edit User',
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
        } else {
          this.$message.warn('Please check the delete option')
        }
        return
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
        title: 'delete confrim?',
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
    this.currentAdminUserName = this.$store.state.user.adminUserName
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
