/**
 * api
 */
import axios from '@/utils/request.js'

const api = {
  addCart: '/myapp/index/cart/create',
  listApi: '/myapp/index/cart/list',
  delCart: '/myapp/index/cart/delete',
}

export const listApi = function (data) {
  return axios({
    url: api.listApi,
    method: 'get',
    params: data
  })
}

export const delCart = function (data) {
  return axios({
    url: api.delCart,
    method: 'post',
    params: data
  })
}

export const addCart = function (data) {
  return axios({
    url: api.addCart,
    method: 'post',
    params: data
  })
}


