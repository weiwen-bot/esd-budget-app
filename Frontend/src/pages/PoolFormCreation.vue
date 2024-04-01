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
    <!-- Error modal popup -->
<div v-if="showErrorModal" class="fixed z-10 inset-0 overflow-y-auto" aria-labelledby="modal-title" role="dialog" aria-modal="true">
  <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center">
    <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="closeErrorModal" aria-hidden="true"></div>

    <!-- Modal panel -->
    <div class="inline-block align-middle bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:max-w-lg sm:w-full" role="document">
      <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
        <div class="sm:flex sm:items-start">
          <!-- Close button wrapper -->
          <div @click="closeErrorModal" class="cursor-pointer absolute top-0 right-0 mt-4 mr-4 text-gray-500 hover:text-gray-800 focus:outline-none">
            <!-- Close button -->
            <button type="button" class="focus:outline-none">
              <span class="sr-only">Close</span>
              <!-- Heroicon name: x -->
              <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Error content -->
          <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left">
            <h3 class="text-lg leading-6 font-medium text-red-500" id="modal-title">
              Error
            </h3>
            <div class="mt-2">
              <p class="text-sm text-gray-900 font-bold">
                {{ errorMessage }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
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
      poolType: '', 
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
      username : '',
      ////////
      showErrorModal: false,
      errorMessage: ''
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
  // Validate pool name
  if (!this.poolName.trim()) {
        this.showErrorMessage("Pool name is required.");
        return;
      }

      // Validate pool type
      if (!this.poolType.trim()) {
        this.showErrorMessage("Pool Type is required.");
        return;
      }

      // Validate target budget
      if (this.targetBudget <= 0 || isNaN(this.targetBudget)) {
        this.showErrorMessage("Target budget must be more than 0.");
        return;
      }
      if (this.targetBudget >= 10000 || isNaN(this.targetBudget)) {
        this.showErrorMessage("Target budget must be less than 10,000.");
        return;
      }

      // Validate expiry date
      if (!this.expiryDate) {
        this.showErrorMessage("Expiry date is required.");
        return;
      }
      const today = new Date();
      const selectedDate = new Date(this.expiryDate);
      if (selectedDate <= today) {
        this.showErrorMessage("Expiry date must be after today's date.");
        return;
      }

      // Validate selected users
      if (this.selectedUsers.length < 1) {
        this.showErrorMessage("At least one participant must be selected.");
        return;
      }

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
    showErrorMessage(message) {
      this.errorMessage = message;
      this.showErrorModal = true;
    },
    closeErrorModal(event) {
  // Close modal only if the click event target is the overlay or the close button
  if (event.target.classList.contains('bg-gray-500') || event.target.closest('.cursor-pointer')) {
    this.errorMessage = '';
    this.showErrorModal = false;
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
