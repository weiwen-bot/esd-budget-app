<template>
  <div>
    <div class="absolute left-15 top-18">
      <router-link to="/" class="text-black hover:text-blue-700 text-lg">&lt;</router-link>
    </div>
    <h1 class="text-2xl font-bold mb-4">Create a New Pool</h1>
    <div class="card grid grid-cols-1 gap-y-4 items-center mt-4"> 
      <div class="flex flex-col items-center"> 
        <label for="poolName" class="mr-2">Pool Name:</label>
        <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white text-center" type="text" id="poolName" v-model="poolName" />
      </div>
      <div class="flex flex-col items-center"> 
        <label for="poolDesc" class="mr-2">Pool Description:</label>
        <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white text-center" type="text" id="poolDesc" v-model="poolDesc" />
      </div>
      <div class="flex flex-col items-center"> 
        <label for="poolType" class="mr-2">Pool Type:</label>
        <select class="shadow appearance-none border rounded w-64 py-2 px-3 text-center text-black leading-tight focus:outline-none focus:shadow-outline bg-white" id="poolType" v-model="poolType">
          <option value="payment">Payment</option>
          <option value="fund">Fund</option>
        </select>
      </div>
      <div class="flex flex-col items-center"> 
        <label for="targetBudget" class="mr-2">Target Budget:</label>
        <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white text-center" type="number" id="targetBudget" v-model="targetBudget" />
      </div>
      <div class="flex flex-col items-center"> 
        <label for="expiryDate" class="mr-2">Expiry Date:</label>
        <input class="shadow appearance-none border rounded w-64 py-2 px-3 text-black leading-tight focus:outline-none focus:shadow-outline bg-white text-center" type="date" id="expiryDate" v-model="expiryDate" />
      </div>
      <div class="flex items-center justify-center">
        <button class="border border-black text-black font-bold py-1 px-2 rounded focus:outline-none focus:shadow-outline text-sm" @click="showUserList =!showUserList">
          Add Participants
        </button>
      </div>
      <div v-if="showUserList" class="mt-4 ">
        <h2 class="text-lg font-semibold mb-2">Users:</h2>
        <div v-for="user in users" :key="user.UserID" class="mb-2">
          <input type="checkbox" v-model="selectedUsers" :value="user.UserID" class="mr-2">
          <span>{{ user.UserName }}</span>
        </div>
      </div>

      <div class="flex items-center justify-center mt-4">
        <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py- px-4 rounded focus:outline-none focus:shadow-outline" @click="createPool">
          Create Pool
        </button>
      </div>
    </div>

    <!-- Success pop-up -->
    <div v-if="showSuccessPopup" class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-lg shadow-lg">
        <p class="text-lg font-semibold text-green-500">Pool created successfully!</p>
        <button @click="hideSuccessPopup" class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-lg focus:outline-none">Close</button>
      </div>
    </div>
  </div>
</template>

<script>

import axios from 'axios';
import { mapStores } from 'pinia';
import { useAuthStore } from '../store/authStore';
import { useUsersStore } from '../store/userStore';

export default { 
  name: 'PoolCreation', 
  data() { 
    return { 
      poolName: '', 
      poolType: 'Payment', 
      targetBudget: '', 
      expiryDate: '',
      poolDesc: '',
      // userList: [ 
      //   { id: 1, name: 'User1' },
      //   { id: 2, name: 'User2' },
      //   { id: 3, name: 'User3' },
      // ],
      showUserList: false,
      selectedUsers: [],
      showSuccessPopup: false,
      users: [],
      userid : '',
      username : ''
    }; 
  },
  computed: {
    // computed
    ...mapStores(useAuthStore),
    ...mapStores(useUsersStore),
  },
  created() {
    this.fetchUsers();
    },
  methods: { 
    async fetchUsers() {
      const authStore = useAuthStore();
      this.userid = authStore.userID
      this.username = authStore.user
      try {
        const response = await fetch('http://127.0.0.1:5004/user');
        const responseData = await response.json();

        if (response.ok) {
          this.users = responseData.data.users;
          const index = this.users.indexOf(username)
          this.users = this.users.splice(index, 1);

          this.showUserList = true;
        } else {
          console.error('Failed to fetch users:', responseData.message);
        }
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    async createPool() {
      // Prepare data to send to the Flask server
      const requestData = {
        pool_name: this.poolName,
        pool_desc: this.poolDesc, // You can add a description field if needed
        Expiry_Date: this.expiryDate,
        Current_amount: 0, // This might be initialized with 0 initially
        Budget: parseFloat(this.targetBudget), // Make sure to parse as float
        Pool_Type: this.poolType,
        UserID: this.userid, // Assuming a default user ID or you need to handle this
        // 
        // GET USERID FROM LOGIN AND CHANGE THE 1
        // 
        Status: 'active' // You may want to set default status or handle it dynamically
      };
      var payload = {"pool_info" : requestData, "pool_invites" : this.selectedUsers}
      try {
        // Make POST request to Flask server
        const response = await fetch('http://127.0.0.1:5100/create_pool', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        });

        // Check if the request was successful
        if (response.ok) {
          // Show success popup
          this.showSuccessPopup = true;

          // Optionally, you can reset form fields here
          this.resetForm();
        } else {
          // Handle error response
          const errorData = await response.json();
          console.error('Failed to create pool:', errorData);
          // Optionally, you can show error message here
        }
      } catch (error) {
        console.error('Error creating pool:', error);
        // Handle network error or other exceptions
      }
    },

    resetForm() {
      // Reset form fields
      this.poolName = '';
      this.poolType = 'payment';
      this.targetBudget = '';
      this.expiryDate = '';
      this.selectedUsers = [];
    },

    hideSuccessPopup() {
      // Hide success pop-up
      this.showSuccessPopup = false;
    }
  }
}
</script> 

<style> 
  
</style>
