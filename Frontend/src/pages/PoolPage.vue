<template>
  <div class="container mx-auto p-4 relative">
    <router-link to="/notification" class="absolute top-4 right-4">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="black" class="w-6 h-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0" />
        </svg>
    </router-link>
    <h1 class="text-2xl font-bold mb-4">Pool List</h1>
    <p v-if="pools.length === 0" class="mb-2">You are not in any pools right now. Check your invite page or create one today!</p>
    <p v-else class="mb-2">You are in <strong>{{ pools.length }}</strong> pools</p>
    <div class="flex justify-center mb-4">
      <router-link to="/poolcreation" class="border border-black text-black font-bold py-2 px-4 rounded hover:bg-black hover:text-white">
        Create Pool
      </router-link>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
      <div v-for="(pool, index) in pools" :key="index" class="border border-gray-400 rounded-md mb-4">
        <div class="bg-white shadow-md rounded-md p-4">
          <div class="border-b-2 border-gray-400 mb-4 pb-2">
            <h2 class="text-lg font-semibold">{{ pool.pool_name }}</h2>
            <h2 class="text-sm font-semibold italic">Created by {{ pool.userName }}</h2>
          </div>
          <div class="mb-4">
            <p class="mb-4"><strong>Current Amount:</strong> ${{ pool.Current_amount }}</p> 
            <p class="mb-4"><strong>Target Amount:</strong> ${{ pool.Budget }}</p> 
          </div>
          <div class="mb-4">
            <div class="progress-bar-container">
              <div class="progress-bar" :style="{ width:  `${calculateProgressPercentage(pool.Current_amount, pool.Budget)}`}"></div>
            </div>
            <p><strong>Progress: {{calculateProgressPercentage(pool.Current_amount, pool.Budget)}}</strong></p>
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

export default {
  name: 'PoolPage',
  data() {
    return {
      stripe: null,
      pools: [
  {
    id: 1,
    name: 'Japan Trip',
    userName: "John44",
    category: 'Fund',
    description: 'Japan Trip after Finals',
    currentAmount: 1200,
    totalAmount: 5000,
  },
  {
    id: 2,
    name: 'Dinner at Mcdonald',
    userName: "Sarah4",
    category: 'Payment',
    description: 'Last night dinner',
    currentAmount: 6000,
    totalAmount: 8000,
    expiryDate:'2024-01-05',
    
  },
],
    }
  },
  computed: {
    //
  },
  methods: {
    viewPool(poolName) {
      this.$router.push({ name: 'IndividualPoolPage', params: { poolName } });
      console.log(`Viewing pool: ${poolName}`);
    },
    async fetchPoolDetails() {
  try {
    const response = await fetch('http://127.0.0.1:5001/Pool');
    if (response.ok) {
      const data = await response.json();
      this.pools = data.data.pools;

      // Fetch usernames for each pool
      // Inside the fetchPoolDetails method
await Promise.all(this.pools.map(async (pool) => {
  try {
    const userResponse = await fetch(`http://127.0.0.1:5004/user/${pool.UserID}`);
    if (userResponse.ok) {
      const userData = await userResponse.json();
      if (userData.code === 200) {
        pool.userName = userData.data.UserName;
      } else {
        console.error('Failed to fetch pool username:', userData.message);
        // If username is unknown, set it to "Unknown (UserID)"
        pool.userName = `Unknown (${pool.UserID})`;
      }
    } else {
      console.error('Failed to fetch pool username:', userResponse.statusText);
      // If username is unknown, set it to "Unknown (UserID)"
      pool.userName = `Unknown (${pool.UserID})`;
    }
  } catch (error) {
    console.error('Error fetching pool username:', error);
    // If username is unknown, set it to "Unknown (UserID)"
    pool.userName = `Unknown (${pool.UserID})`;
  }
}));

    } else {
      console.error('Failed to fetch pool details:', response.statusText);
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
    calculateProgressPercentage(currentAmount, totalAmount) {
      return (currentAmount / totalAmount) * 100 + '%';
    },
  },
  components: {},
  created() {
    // Calculate progress percentage and fetch data on component creation
    this.pools.forEach((pool) => {
      pool.progressPercentage = this.calculateProgressPercentage(pool.currentAmount, pool.totalAmount);
    });
    this.fetchPoolDetails();
    this.fetchTransactionHistory();
  },
};
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