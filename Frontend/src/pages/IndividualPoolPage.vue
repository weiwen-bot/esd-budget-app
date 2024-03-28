<template>
  <div>
    <h1>Pool Details</h1>
    <div>
      <p><strong>Pool Name:</strong> {{ pool.pool_name }}</p>
      <p><strong>Category:</strong> {{ pool.Pool_Type }}</p>
      <p><strong>Description:</strong> {{ pool.pool_desc }}</p>
      <div>
        <p><strong>Current Amount:</strong> ${{ pool.Current_amount }}</p>
        <p><strong>Total Amount:</strong> ${{ pool.Budget }}</p>
        <p><strong>Progress:</strong></p>
        <div class="progress-bar-container">
          <div class="progress-bar" :style="{ width: progressPercentage() }"></div>
        </div>
      </div>
      <h2>Transaction History</h2>
      <ul>
        <li v-for="transaction in transactions" :key="transaction.id">
          {{ transaction.date }} - {{ transaction.amount }} - {{ transaction.description }}
        </li>
      </ul>
      <button @click="makePayment">Make Payment</button>
    </div>
  </div>
</template>
  
  <script>
export default {
  name: 'IndividualPoolPage',
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
    progressPercentage() {
      if (this.pool) {
        return `${(this.pool.pool_Current_amount / this.pool.Budget) * 100}%`;
      }
      return '0%';
    },
    async fetchPoolDetails() {
      try {
        const response = await fetch('http://localhost:8000/pool/2'); // Replace '2' with the actual pool ID
        const data = await response.json();
        if (response.ok) {
          this.pool = data.data;
        } else {
          console.error('Failed to fetch pool details:', data.message);
        }
      } catch (error) {
        console.error('Error fetching pool details:', error);
      }
    },
    async fetchTransactionHistory() {
      try {
        const response = await fetch('http://localhost:5005/TransactionHistory/1'); // Replace '1' with the actual pool ID
        const data = await response.json();
        if (response.ok) {
          this.transactions = data.data.transactions;
        } else {
          console.error('Failed to fetch transaction history:', data.message);
        }
      } catch (error) {
        console.error('Error fetching transaction history:', error);
      }
    },
    async makePayment() {
      try {
        const response = await fetch('http://localhost:5100/pool_management', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            poolID: 2, // Replace '2' with the actual pool ID
            userID: 1, // User ID = 1 
            amount: 100 // Replace '100' with the actual payment amount
          })
        });
            const data = await response.json();
            if (response.ok) {
            alert('Payment successful');
            // Optionally, you can update the pool details or transaction history after payment
            // this.fetchPoolDetails();
            // this.fetchTransactionHistory();
            } else {
            console.error('Failed to make payment:', data.message);
            }
        } catch (error) {
            console.error('Error making payment:', error);
        }
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
  