<template>
  <div class="header">
    <img class="header-logo" src="@/assets/images/front-logo.png">
    <span class="header-title">{{ lang.platform[this.$store.state.language] }}</span>
    <div class="empty"></div>
    <span>{{ lang.admin[this.$store.state.language] }}[{{$store.state.user.adminUserName}}]</span>
    <a class="header-quit" @click="handleLogout">{{ lang.logout[this.$store.state.language] }}</a>
  </div>
</template>

<script>
import langData from '@/lang/lang.json'

export default {
  name: 'Header',
  data () {
    return {
      username: '',
      lang: langData
    }
  },
  mounted () {
    // this.username = this.$store.state.user.adminUserName
    this.locale()
  },
  methods: {
    locale () {
      return this.$store.state.language;
    },
    handleLogout () {
      this.$store.dispatch('AdminLogout').then(res => {
        this.$router.push({path: '/admin-login'})
      })
    }
  }
}
</script>
<style lang="less" scoped>

.header {
  display: flex;
  flex-direction: row;
  align-items: center; // 垂直居中
  padding-left: 24px;
  padding-right: 24px;

  .header-logo {
    width: 32px;
    height: 32px;
    cursor: pointer;
  }

  .header-title {
    margin-left: 16px;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
  }

  .empty {
    flex:1;
  }

  .header-quit {
    margin-left: 12px;
  }
}
</style>
