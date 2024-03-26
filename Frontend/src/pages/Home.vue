<template>
  <div>
    
    <template>
  <nav class="navbar">
    <div class="brand">
      <router-link to="/">
        <img src="/src/assets/pool_service_logo.png" class="h-14 mr-4 rounded-3xl" alt="PoolService Logo" />
      </router-link>
    </div>
    <button data-collapse-toggle="navbar-multi-level" type="button"
            class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-200 rounded-lg lg:hidden hover:bg-neutral-500 focus:outline-none focus:ring-2 focus:ring-neutral-500"
            aria-controls="navbar-multi-level" aria-expanded="false">
      <span class="sr-only">Open main menu</span>
      <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M1 1h15M1 7h15M1 13h15" />
      </svg>
    </button>
    <div class="hidden w-full lg:block lg:w-auto" id="navbar-multi-level">
      <ul class="menu">
        <li>
          <div>
            <label for="nav-search" class="mb-2 text-xs font-medium text-gray-900 sr-only dark:text-white">Search</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                </svg>
              </div>
              <input type="search" id="nav-search" v-model="to_search" v-on:keyup="check()" placeholder='Search Experiences!' class="block w-full p-2 pl-8 pr-12 mx10 text-xs text-gray-900 border border-slate-900 rounded-lg bg-grey-200" required>
              <button @click="search()" class="text-white absolute right-1 bottom-1 bg-neutral-400 hover:bg-neutral-500 focus:ring-4 focus:outline-none focus:ring-[#50A060] font-xsmall rounded-md text-xs px-1 py-1">Search</button>
            </div>
          </div>
        </li>
        <li>
          <router-link to="/" class="block py-2 pl-3 pr-4 text-white rounded hover:bg-neutral-500 md:hover:bg-transparent md:hover:text-[#50A060] md:p-0" aria-current="page">Home</router-link>
        </li>
        <li>
          <router-link to="/cart" class="block py-2 pl-3 pr-4 text-white rounded hover:bg-neutral-500 md:hover:bg-transparent md:border-0 md:hover:text-[#50A060] md:p-0">Listings</router-link>
        </li>
        <li>
          <router-link to="/itinerary" class="block py-2 pl-3 text-white rounded hover:bg-neutral-500 md:hover:bg-transparent md:border-0 md:hover:text-[#50A060] md:p-0">Itinerary</router-link>
        </li>
        <li>
          <router-link to="/favourites" class="block py-2 pl-3 text-white rounded hover:bg-neutral-500 md:hover:bg-transparent md:border-0 md:hover:text-[#50A060] md:p-0">Favourites</router-link>
        </li>
        <li>
          <button id="dropdownNavbarLink" data-dropdown-toggle="dropdownNavbar" class="flex items-center justify-between w-full py-2 pl-3 pr-4 text-white border border-gray-100 hover:bg-[#50A060] md:hover:bg-transparent md:border-0 md:hover:text-[#50A060] md:p-0 md:w-auto">
            <img src="/src/assets/User Profile Icon.png" />
            <svg class="w-2.5 h-2.5 ml-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4" />
            </svg>
          </button>
          <!-- Dropdown menu -->
          <div id="dropdownNavbar" class="z-10 hidden font-normal bg-white divide-y
          <ul class="py-2 text-sm text-gray-700 dark:text-gray-400" aria-labelledby="dropdownLargeButton">
            <li>
              <SignOutButton to="/login" :isUserSignedIn="isUserSignedIn" @signOut="handleSignOut" class="block px-4 py-2 text-sm text-gray-700 hover:bg-emerald-700 dark:hover:bg-gray-600 dark:text-gray-400 hover:text-white">
                {{ isUserSignedIn ? 'Sign Out' : 'Sign In' }}
              </SignOutButton>
            </li>
          </ul>
        </div>
      </li>
    </ul>
  </div>
</div>
</nav>
</template>

<script>
import router from "../routes";
import SignOutButton from "../components/SignOutButton.vue";
import { ref } from "vue";

export default {
  name: 'Navbar',
  data() {
    return {
      to_search: '',
      isUserSignedIn: false
    };
  },
  created() {
    // Check the user's sign-in status based on your authentication logic
    // For example, if you're using Firebase Authentication:
    onAuthStateChanged(auth, (user) => {
      if (user) {
        // User is signed in
        this.isUserSignedIn = true;
      } else {
        // User is not signed in
        this.isUserSignedIn = false;
      }
    });
  },
  methods: {
    check() {
      console.log(this.to_search)
    },
    search() {
      console.log("searching for: " + this.to_search)
      const value = this.to_search
      searchQuery.updatesearch(value)
      const url = '/search/' + this.to_search
      this.$router.push(url)
    },
    handleSignOut() {
      // Perform sign-out logic here
      signOut(auth)
        .then(() => {
          // Sign-out successful.
          alert('Logged Out successfully!');
          this.isUserSignedIn = false;
          currentID.updateCurrentID('');
          console.log('Logged Out UserID: ' + currentID.currentID)
          currentUser.updateCurrentUser('', 'Anonymous');
          console.log('Logged Out User ID: ' + currentUser.UserID)
          console.log('Logged Out Username: ' + currentUser.UserName)
          // Redirect user back to Log-In page
          router.push('/login');
        })
        .catch((error) => {
          // An error happened.
          console.log(error);
          const errorMessage = error.message;
          alert(errorMessage);
        });
    },
  },
  components: {
    SignOutButton
  }
};
</script>
<style></style>
