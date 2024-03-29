<template>
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Pool List</h1>
    <p v-if="pools.length === 0" class="mb-2">You are not in any pools right now. Check your invite page or create one today!</p>
    <p v-else class="mb-2">You are in <strong>{{ pools.length }}</strong> pools</p>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <div v-for="(pool, index) in pools" :key="index" class="border border-gray-400 rounded-md mb-4">
        <div class="bg-white shadow-md rounded-md p-4">
          <div class="border-b-2 border-gray-400 mb-4 pb-2">
            <h2 class="text-lg font-semibold">{{ pool.name }}</h2>
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
          <div class="flex justify-center mb-4">
            <button @click="viewPool(poolName)" class="view-pool-btn">
              View Pool
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<!-- PoolID = db.Column(db.Integer, primary_key=True,autoincrement=True)
DateCreation = db.Column(db.Date,nullable=False, default=datetime.now)
Expiry_Date = db.Column(db.Date, nullable=False)
Current_amount = db.Column(db.Float, nullable=False)
Budget = db.Column(db.Float, nullable=False)
Pool_Type = db.Column(db.String(36), nullable=False)
UserID = db.Column(db.Integer, nullable=False)
Status = db.Column(db.String(36), nullable=False) -->




<script> 
import axios from 'axios';
export default {
  name: 'PoolPage',
  data() {
    return {
      stripe: null,
      pools: [
  {
    id: 1,
    name: 'Japan Trip',
    category: 'Fund',
    description: 'Japan Trip after Finals',
    currentAmount: 1200,
    totalAmount: 5000,
    expiryDate:'2025-01-03',
    transactions: [
      { id: 1, date: '2022-01-01', amount: 800, description: 'Transaction 1' },
      { id: 2, date: '2022-01-05', amount: 200, description: 'Transaction 2' },
      { id: 3, date: '2022-01-06', amount: 200, description: 'Transaction 3',userID: 1 }
      // Add more transactions as needed
    ],
  },
  {
    id: 2,
    name: 'Dinner at Mcdonald',
    category: 'Payment',
    description: 'Last night dinner',
    currentAmount: 6000,
    totalAmount: 8000,
    expiryDate:'2024-01-05',
    transactions: [
      { id: 3, date: '2022-01-10', amount: 1000, description: 'Transaction 3' },
      { id: 4, date: '2022-01-15', amount: 500, description: 'Transaction 4' },
      // Add more transactions as needed
    ],
  },
  // Add more pools as needed
],
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


<style>
.container {
  margin-left: auto;
  margin-right: auto;
  padding-left: 1rem;
  padding-right: 1rem;
}

.text-2xl {
  font-size: 1.5rem;
}

.font-bold {
  font-weight: 700;
}

.mb-4 {
  margin-bottom: 1rem;
}

.border {
  border-width: 2px;
}

.rounded-md {
  border-radius: 0.375rem;
}

.shadow-md {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.p-4 {
  padding: 1rem;
}

.text-lg {
  font-size: 1.125rem;
}

.font-semibold {
  font-weight: 600;
}

.mb-2 {
  margin-bottom: 0.5rem;
}

.flex {
  display: flex;
}

.justify-between {
  justify-content: space-between;
}

.py-2 {
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.px-4 {
  padding-left: 1rem;
  padding-right: 1rem;
}

.view-pool-btn {
  background-color: #3b82f6;
  color: #fff;
  font-weight: 700;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
}

.view-pool-btn:hover {
  background-color: #2563eb;
}

.progress-bar-container {
  width: 100%;
  background-color: #e5e7eb;
  border-radius: 0.375rem;
}

.progress-bar {
  height: 0.75rem;
  background-color: #4caf50;
  border-radius: 0.375rem;
}

ul {
  list-style-type: none;
  padding-left: 0;
}

li {
  margin-bottom: 0.5rem;
}


@media (min-width: 576px) {
  .grid-cols-1 {
    grid-template-columns: repeat(1, minmax(0, 1fr));
  }
  .grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  .grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}
</style>