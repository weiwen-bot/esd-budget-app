<template>
  <div class="container mx-auto p-4 relative">

    <div class="absolute left-6">
      <router-link to="/" class="text-black hover:text-blue-700 text-lg">&lt; </router-link>   
    </div>
    <h1 class="text-2xl font-bold mb-4">Pool Owner Page</h1>
    <div class="bg-white shadow-md rounded-md p-4">
      <div class="border-b-2 border-gray-400 mb-4 pb-2">
        <h2 class="text-lg font-semibold">{{ pool.name }} 
          <button @click="toggleModal" style="margin: 0px; padding: 0px;">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
              <image href="../assets/Pool_Participant.png" width="24" height="24" />
            </svg>
          </button>

        </h2>
        <h2 class="text-sm font-semibold italic">Created by you!</h2>
      </div>
      <div class="flex justify-center mb-3">
        <router-link to="/inviteusers" class="border border-black text-black font-bold py-1 px-2 rounded text-sm hover:bg-black hover:text-white">Invite to Pool</router-link>
      </div>
      <div class="mb-4">
        <p class="mb-4"><strong>Description:</strong><br> {{ pool.description }}</p>
        <p class="mb-4"><strong>Category:</strong><br>{{ pool.category }}</p>
        <p class="mb-4"><strong>Expiry Date:</strong><br>{{ pool.expiryDate }}</p>  
      </div>
      <div class="mb-4">
        <p><strong>Progress:</strong></p>
        <p>${{ pool.currentAmount }} / ${{ pool.totalAmount }}</p>
        <div class="progress-bar-container">
          <div class="progress-bar" :style="{ width: `${pool.currentAmount/pool.totalAmount * 100}%` }"></div>
        </div>
      </div>
      <div class="flex justify-center mb-4 space-x-4">
        <div class="mb-4 flex justify-center space-x-4">
          <button v-if="pool.category === 'Fund'" @click="contribute" class="btn bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Contribute</button>
          <button v-if="pool.category === 'Fund'" @click="makePayment" class="btn bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Make Payment</button>
          <button v-if="pool.category === 'Payment'" @click="reimburse" class="btn bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Reimburse</button>
          <button @click="deletePool" class="btn bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">Delete Pool</button>
        </div>
      </div>
      <p class="mb-4"><strong>Transaction History:</strong><br></p>
      <div class="overflow-x-auto">
        <table class="table-auto w-full">
          <thead>
            <tr>
              <th class="border px-4 py-2">Date</th>
              <th class="border px-4 py-2">UserID</th>
              <th class="border px-4 py-2">Amount</th>
              <th class="border px-4 py-2">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(transaction, index) in transactions" :key="transaction.id" :class="{ 'bg-gray-300': index % 2 === 0 }">
              <td class="border px-4 py-2">{{ transaction.date }}</td>
              <td class="border px-4 py-2">{{ transaction.userID }}</td>
              <td class="border px-4 py-2">${{ transaction.amount }}</td>
              <td class="border px-4 py-2">{{ transaction.description }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="toggleModal">&times;</span>
        <h2 class="text-center"><strong>Participants</strong></h2>
        <p>There are {{ users.length }} participants</p>
        <table class="border-collapse border border-gray-400">
    <thead>
      <tr>
        <th class="border border-gray-400 px-4 py-2">S/N</th>
        <th class="border border-gray-400 px-4 py-2">Username</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(user, index) in users" :key="index" class="border border-gray-400">
        <td class="border border-gray-400 px-4 py-2">{{ index + 1 }}</td>
        <td class="border border-gray-400 px-4 py-2">{{ user }}</td>
      </tr>
    </tbody>
  </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OwnerPoolPage',
  data() {
    return {
      pool: {
        id: 1,
        name: 'Mcdonald dinner',
        category: 'Fund',
        description: 'Mcdonald Meal for 10',
        currentAmount: 1200,
        totalAmount: 5000,
        expiryDate: '2025-01-03'
      },
      users: ['232323', '2323232', '2323'], 
  
      showModal: false,

      transactions: [
        { id: 1, date: '2022-01-01', amount: 800, description: 'Transaction 1',userID:3 },
        { id: 2, date: '2022-01-05', amount: 200, description: 'Transaction 2',userID: 1 },
        { id: 3, date: '2022-01-06', amount: 200, description: 'Transaction 3',userID: 1 }
      ]
    };
  },
  created() {
    // Fetch initial data
  },
  methods: {
   
    toggleModal() {
      this.showModal = !this.showModal;
    },
    async contribute() {
      // Contribute logic
    },
    async makePayment() {
      // Make payment logic
    },
    async reimburse() {
      // Reimburse logic
    },
    deletePool() {
      // Delete pool logic
    }
  }
};
</script>

<style>
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  border-radius: 0.375rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  z-index: 1000;
  max-width: 500px; 
}

.modal-content {
  background-color:white;
  padding: 50px;
  border: 1px solid #888;
  text-align:center;
  width: 100%;
}

.close {
  color: #aaa;
  position: absolute;
  top: 1rem; 
  right: 1rem; 
  font-size: 1.5rem;
  font-weight: bold;
  cursor: pointer;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>
