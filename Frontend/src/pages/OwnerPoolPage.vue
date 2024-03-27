<template>
    <div>
      <h1>Pool Details</h1>
      <div>
        <p><strong>Pool Name:</strong> {{ pool && pool.name }}</p>
        <p><strong>Category:</strong> {{ pool && pool.category }}</p>
        <p><strong>Description:</strong> {{ pool && pool.description }}</p>
        <div>
          <p><strong>Current Amount:</strong> ${{ pool && pool.currentAmount }}</p>
          <p><strong>Total Amount:</strong> ${{ pool && pool.totalAmount }}</p>
          <p><strong>Progress:</strong></p>
          <div class="progress-bar-container">
            <div class="progress-bar" :style="{ width: progressPercentage }"></div>
          </div>
        </div>
        <h2>Transaction History</h2>
        <ul>
          <li v-for="transaction in transactions" :key="transaction.id">
            {{ transaction.date }} - {{ transaction.amount }} - {{ transaction.description }}
          </li>
        </ul>
        <button @click="makePayment">Make Payment</button>
        <button @click="refund">Refund</button>
        <button @click="collect">Collect</button>
        <button @click="deletePool">Delete</button>
      </div>
    </div>
  </template>
  
  
  <script>
  export default {
    name: 'OwnerPoolPage',
    data() {
      return {
        pool: null,
        transactions: []
      };
    },
    created() {
      this.fetchPoolDetails();
      this.fetchTransactionHistory();
    },
    methods: {
      async fetchPoolDetails() {
        // Fetch pool details from backend
      },
      async fetchTransactionHistory() {
        // Fetch transaction history from backend
      },
      async makePayment() {
        // Make payment logic
      },
      refund() {
        // Refund logic
      },
      collect() {
        // Collect logic
      },
      deletePool() {
        // Delete pool logic
      }
    }
  };
  </script>
  
  <style>
  .progress-bar-container {
    width: 100%;
    background-color: #f0f0f0;
  }
  
  .progress-bar {
    height: 20px;
    background-color: #007bff;
  }
  </style>
  