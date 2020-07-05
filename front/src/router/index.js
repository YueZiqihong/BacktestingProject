import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Backtesting from '@/components/Backtesting'
import uploader from '@/components/uploader'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path:'/backtesting',
      name:'backtesting',
      component: Backtesting
    },
    {
      path: '/upload',
      name: 'uploader',
      component: uploader
    },
  ]
})
