<template>
  <div id="app">

    <div class="container mx-auto px-4 py-8">
      <h1 class="text-2xl font-sans font-bold text-center mb-8">Pool List</h1>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
        <div v-for="(pool, index) in pools" :key="index" class="rounded-lg card shadow-lg">
          <div class="card-content card-content-top">
            <div class="card-title">
              {{ pool.name }}
            </div>
          </div>
          
          <span class="progress-text">
              <a>Progress: {{ pool.progressPercentage }}</a>
          </span>
          
          <div class="card-progress-bar">

            <div class="card-progress-bar-fill" :style="{ width: pool.progressPercentage }"></div>
          </div>
          <div class="card-description">
            {{ pool.description }}
          </div>
          <div class="card-amounts">
            <div class="current-amount">
              <a style="font-size: 15px;"> Current Amount: ${{ pool.currentAmount }}</a>
            </div>
            <div class="total-amount">
              <a style="font-size: 15px; ">Total Amount: ${{ pool.totalAmount }}</a>
            </div>
            
          </div>
          <div class="button-group">
            <button @click="viewPool(pool.name)" class="view-pool">
              View Pool
            </button>
          </div>
          

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PoolPage',
  data() {
    return {
      stripe: null,
      pools: [
        {
          name: 'Pool 1',
          category: 'Category 1',
          description: 'Trip to Bangkok',
          currentAmount: '9000',
          totalAmount: '10000',
          transactionHistory: [
            {
              id: 1,
              date: '2023-03-24',
              amount: '100',
              description: 'Transaction 1',
            },
            {
              id: 2,
              date: '2023-03-25',
              amount: '150',
              description: 'Transaction 2',
            },
          ],
        },
        {
          name: 'Pool 2',
          category: 'Category 2',
          description: 'Weekend Buffet',
          currentAmount: '3000',
          totalAmount: '20000',
          transactionHistory: [
            {
              id: 3,
              date: '2023-03-24',
              amount: '200',
              description: 'Transaction 3',
            },
          ],
        },
      ],
    };
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
      // API call to fetch pool details
    },
    async fetchTransactionHistory() {
      // API call to fetch transaction history
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