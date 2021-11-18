
const routes = [
  {
    path: '/',
    component: () => import('layouts/LoginLayout.vue'),
    children: [
      {
        path: '',
        name: 'login',
        component: () => import('pages/Index.vue')
      }
    ]
  },

  {
    path: '/dashboard',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'dashboard',
        component: () => import('pages/Dashboard.vue')
      },
      {
        path: '/dashboard/search',
        name: 'search',
        component: () => import('pages/Search.vue')
      },
      {
        path: '/dashboard/tasks/site_activation',
        name: 'site_activation',
        component: () => import('pages/SiteActivation.vue')
      }
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/Error404.vue')
  }
]

export default routes
