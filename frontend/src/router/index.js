// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'sign-in',
    component: () => import('@/views/SignInPage.vue'),
  },
  {
    path: '/masterlist',
    name:'masterlist',
    component: () => import('@/views/MasterList.vue'),
    meta: { requiresAuth: true }
  },
  {
    name:'courses',
    path: '/courses',
    component: () => import('@/views/Courses.vue'),
    meta: { requiresAuth: true }
  },
  {
    name:'schedules',
    path: '/schedules',
    component: () => import('@/views/Schedules.vue'),
    meta: { requiresAuth: true }
  },
  {
    name:'register',
    path: '/register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: true }
  },
  {
    name:'settings',
    path: '/settings',
    component: () => import('@/views/UserSettings.vue'),
    meta: { requiresAuth: true }
  },
  {
    name:'dashboard',
    path:'/dashboard',
    component: () => import('@/views/Dashboard.vue'),
    meta: {requiresAuth: true}
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

// Middleware/Interceptor to check authentication
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Check if the user is authenticated
    const token = localStorage.getItem('token');
    const userType = localStorage.getItem('user_type');
    if (!token) {
      // If not authenticated, redirect to login page with proper redirection path
      next({ path: '/', query: { redirect: to.fullPath } });
    } else if (to.name === 'register' && userType !== 'administrator') {
      // If the requested route is 'register' and user is not an administrator, redirect to dashboard or any other appropriate route
      next({ path: '/dashboard' }); // Redirect to dashboard or any other appropriate route
    } else {
      // If authenticated, proceed to the requested route
      to.meta.showNavigationDrawer = true;
      next();
    }
  } else {
    // For routes that don't require authentication, proceed as usual
    next();
  }
});

export default router
