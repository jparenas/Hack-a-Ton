import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Search from '@/components/Search'
import ShowPage from '@/components/ShowPage'

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/search',
      name: 'Search',
      component: Search,
    },
    {
      path: '/show',
      name: 'ShowPage',
      component: ShowPage,
      props: (route) => ({
        origin: route.query.origin
      })
    }
  ]
})