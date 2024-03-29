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
<style>
  :root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.87);
  --primary-color: #007bff; ;
  --card-background-color: #ffffff;
  --card-border-color: #e0e0e0;
  --card-padding: 1.5em;
  --card-text-color: #213547;
  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a {
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}
a:hover {
  color: #535bf2;
}

body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
}

h1 {
  font-size: 1.5em;
  line-height: 1.1;
}

button {
  border-radius: 8px;
  border: 1px solid transparent;
  padding: 0.6em 1.2em;
  font-size: 1em;
  font-weight: 500;
  font-family: inherit;
  background-color: #1a1a1a;
  cursor: pointer;
  transition: border-color 0.25s;
  color: white;
  width: 250px;
}
button:hover {
  border-color: #646cff;
}
button:focus,
button:focus-visible {
  outline: 4px auto -webkit-focus-ring-color;
}

/* .card {
  padding: 2em;
} */

#app {
  max-width:1200px;
  margin: auto;
  padding: 2rem;
  text-align: center;
}

.card {
  background-color: var(--card-background-color);
  border: 1px solid var(--card-border-color);
  padding: var(--card-padding);
  border-radius: 4px;
  color: var(--card-text-color);
  margin-bottom: 1.5rem;
}

.card-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-bottom: 1rem;
}

.card-content-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;

}

.card-title {
  font-size: 1rem;
  font-weight: 600;
  margin-top:10px;
}

.card-description {
  line-height: 1.5;
  margin-bottom: 1rem;
  color:black;
  font-weight: bold;
}

.card-amounts{
  color:black;
  text-align:justify;
  font-weight: bold;
}

.button-group {
  display: flex;
  align-items: center;
  margin-top: 0.3rem;
  justify-content: center;
}

.view-pool{
  display: flex;
  align-items: center;
  justify-content: center;
  width: 150px;

  
}

.card-progress-bar {
  height: 10px;
  background-color: #f5f5f5;
  overflow: hidden;
  border-radius: 5px;
  margin-top: 10px;
  width:100%;
  border: grey solid 1px;
}

.card-progress-bar-fill {
  height: 10px;
  background-color: #007bff;
  width: v-bind("pool.progressPercentage");
  position: relative;
  display: block;
  border-radius: 5px;
}

.progress-text{
  text-align:end;
  font-size: 15px;
  margin-top:10px;

}
@media (min-width: 768px) {
  .card-content-top {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }

  .card-content {
    align-items: center;
  }

  .card {
    display: grid;
    grid-template-columns: auto 1fr;
    grid-gap: 1rem;
  }
}
.card-title {
  grid-column: 1 / 3;
  margin-bottom: 0;
}

.button-group {
  grid-column: 2;
}

.card-description {
  grid-column: 1 / 3;
}

.card-progress-bar {
  grid-column: 1 / 3;
}


@media (prefers-color-scheme: light) {
  :root {
    color: #213547;
    background-color: #ffffff;
    --card-background-color: #f9f9f9;
    --card-text-color: #213547;
  }
  a:hover {
    color: #747bff;
  }
  button {
    background-color: #f9f9f9;
  }
  
}

</style>