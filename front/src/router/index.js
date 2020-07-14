import Vue from 'vue'
import Router from 'vue-router'
import Homepage from '@/components/Homepage'
import Backtesting from '@/components/Backtesting'
import StockPool from '@/components/StockPool'
import Uploader from '@/components/Uploader'
import Search from '@/components/Search'
import Portfolio from '@/components/Portfolio'
import Market from '@/components/Market'
import Transaction from '@/components/Transaction'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Homepage
    },
    {
      path:'/backtesting',
      name:'backtesting',
      component: Backtesting
    },
    {
      path: '/upload',
      name: 'Uploader',
      component: Uploader
    },
    {
      path: '/pool',
      name: 'StockPool',
      component: StockPool
    },
    {
      path:'/search',
      name:'Search',
      component: Search
    },
    {
      path:'/portfolio',
      name:'Portfolio',
      component: Portfolio
    },
    {
      path:'/market',
      name:'Market',
      component: Market
    },
    {
      path:'/transaction',
      name:'Transaciton',
      component: Transaction
    },

  ]
})
