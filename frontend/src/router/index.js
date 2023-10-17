import Vue from 'vue'
import VueRouter from 'vue-router'
// import AppV from '../App.vue'
import AdminLogin from '../views/AdminLogin.vue'
import UserLogin from '../views/UserLogin.vue'
import AdminRegister from '../views/AdminReg.vue'
import UserRegister from '../views/UserReg.vue'
import AdminDash from '../views/AdminDash.vue'
import UserDash from '../views/UserDash.vue'
import Logout from '../views/Logout.vue'; // Corrected filename to 'Logout.vue'
import Summary from '../views/Summary.vue';
import Bookings from '../views/Bookings.vue'
import Profile from '../views/Profile.vue'


Vue.use(VueRouter)

const routes = [
  // {
  //   path: '/hello',
  //   name: 'a',
  //   component: AppV
  // },
  {
    path: "/admin",
    name: "admin",
    component: AdminLogin,
  },
  {
    path: "/user",
    name: "user",
    component: UserLogin,
  },
  {
    path: "/admin_reg",
    name: "admin_reg",
    component: AdminRegister,
  },
  {
    path: "/user_reg",
    name: "user_reg",
    component: UserRegister,
  },
  {
    path: "/admin_dashboard",
    name: "admin_dashboard",
    component: AdminDash,
  },
  {
    path: "/summary",
    name: "summary",
    component: Summary,
  },
  {
    path: "/bookings",
    name: "Boo-kings",
    component: Bookings,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/user_dashboard",
    name: "user_dashboard",
    component: UserDash,
  },
  {
    path: "/logout",
    name: "logout",
    component: Logout,
  },
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
