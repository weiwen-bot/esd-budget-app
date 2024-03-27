<template> 
  <div class="container mx-auto p-4"> 
    <h1 class="text-2xl font-bold mb-4">Pool List</h1> 
    <div v-for="(pool, index) in pools" :key="index" class="border border-black rounded-md mb-4"> 
      <div class="bg-white shadow-md rounded-md p-4"> 
        <h2 class="text-lg font-semibold mb-2">{{ pool }}</h2>
        <div class="flex justify-between mb-4">
          <button @click="viewPool(poolName)" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
            View Pool
          </button>
        </div>
        <div class="mb-4">
          <p><strong>Pool Name:</strong> {{ pool.name }}</p>
          <p><strong>Category:</strong> {{ pool.category }}</p>
          <p><strong>Description:</strong> {{ pool.description }}</p>
        </div>
        <div class="mb-4">
          <p><strong>Current Amount:</strong> ${{ pool.currentAmount }}</p>
          <p><strong>Total Amount:</strong> ${{ pool.totalAmount }}</p>
          <p><strong>Progress:</strong></p>
          <div class="progress-bar-container">
            <div class="progress-bar" :style="{ width: progressPercentage }"></div>
          </div>
        </div>
        <h2 class="mb-2">Transaction History</h2>
        <ul>
          <li v-for="transaction in transactions" :key="transaction.id">
            {{ transaction.date }} - {{ transaction.amount }} - {{ transaction.description }}
          </li>
        </ul>
      </div>
    </div> 
  </div> 
</template>



 

  <!-- <div> 
      <h1>HOME</h1> 
      <button 
                  type="button" 
                  class="btn btn-primary btn-sm" 
                  @click="handlePurchaseBook(book)"> 
                  Purchase 
                </button> 
  </div> 
  <h1>Add Components</h1>  -->



<script> 
import axios from 'axios';
export default {
  name: 'PoolPage',
  data() {
    return {
      stripe: null,
      pools: ['Pool 1', 'Pool 2', 'Pool 3'],
      transactions: []
    }
  },
  computed: {
  },
  methods: {
    viewPool(poolName) { 
      this.$router.push({ name: 'IndividualPoolPage', params: { poolName } });
      console.log(`Viewing pool: ${poolName}`); 
    },
    async fetchPoolDetails() {
      try {
        const response = await fetch('http://localhost:5005/Pool/1'); // Replace '1' with the actual pool ID
        const data = await response.json();
        if (response.ok) {
          this.pools = data.data;
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
    getStripePublishableKey() {
      fetch('http://localhost:4242/config')
        .then((result) => result.json())
        .then((data) => {
          // Initialize Stripe.js
          this.stripe = Stripe(data.publicKey);
        });
    },
    handlePurchaseBook() {
      // Get Checkout Session ID
      fetch('http://127.0.0.1:4242/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ book_id: '2' }),
      })
        .then((result) => result.json())
        .then((data) => {
          console.log(data);
          // Redirect to Stripe Checkout
          return this.stripe.redirectToCheckout({ sessionId: data.sessionId });
        })
        .then((res) => {
          console.log(res);
        });
    },
  },
  components: {},
  created() {
    this.getStripePublishableKey();
    this.fetchPoolDetails();
    this.fetchTransactionHistory();
  },
}
</script>
