<template>
    <nav class="bg-white-800 p-4">
      <div class="max-w-7xl mx-auto">
        <div class="flex justify-center">
          <div class="flex space-x-4">
            <ul class="flex border-b">
              <!-- Navigation Links -->
              
              <li class="mr-1">
                <router-link to="/poolcreation" exact active-class="bg-blue-500 border-l border-t border-r rounded-t" class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold">Create Pool</router-link>
              </li>
              <li class="-mb-px mr-1">
                <router-link to="/" exact active-class="bg-blue-500 border-1 border-t border-r rounded-t" class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold">Pool Page</router-link>
              </li>
              <li class="mr-1">
                <router-link to="/notification" exact active-class="bg-blue-500 border-l border-t border-r rounded-t" class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold">Notifications</router-link>
              </li>
              <li v-if="userid === null">
                <router-link to="/login" exact active-class="bg-blue-500 border-l border-t border-r rounded-t" class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold">Login</router-link>
                </li>
                <li v-else>
                  <p>{{ this.username }}</p>
                  <button @click="logout()" exact active-class="bg-blue-500 border-l border-t border-r rounded-t" class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold" >LOGOUT</button>
                </li>
                
                
            </ul>
          </div>
        </div>
      </div>
    </nav>
  </template>
  
  <script>

import axios from 'axios';
import { mapStores } from 'pinia';
import { useAuthStore } from '../store/authStore';
import { useUsersStore } from '../store/userStore';

  export default {
    name: "NavBar",
    // Add any necessary logic here
    computed: {
    // computed
    ...mapStores(useAuthStore),
    ...mapStores(useUsersStore),
  },
  data() { 
    return { 
      userid : '',
      username: 0
    }; 
  },
  created() {
    this.fetchUsers();
    },
    methods: { 
    async fetchUsers() {
      const authStore = useAuthStore();
      this.userid = authStore.userID
      this.username = authStore.user
      console.log(this.userid,'userid')
    },

    async logout() {
      const authStore = useAuthStore();
      authStore.logout();
      await this.fetchUsers();
      // this.$router.push('/poolcreation');
      this.redirectReload('/poolcreation')
    },
    redirectReload(path_l) {
        this.$router
          .push({ path: path_l })
          .then(() => { this.$router.go(0) })
      }
  }
  }
  </script>
  
  <style>
  /* Add any custom styles here */
  </style>
  