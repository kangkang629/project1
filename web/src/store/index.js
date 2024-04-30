import Vue from 'vue'
import Vuex from 'vuex'
// import {listApi} from '@/api/admin'

import user from './modules/user'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    language: localStorage.getItem('language') || 'en'
  }, // 存放数据
  getters: {}, // 计算属性
  mutations: {
    SET_LAN(state, language) {
      state.language = language
      localStorage.setItem('language', language)
    }
  }, // 修改state中数据的一些方法
  actions: {
    setLan({ commit }, language) {
      commit('SET_LAN', language);
    }
  }, // 异步方法
  modules: {
    user
  }
})
