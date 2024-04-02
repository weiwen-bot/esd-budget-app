<template>
    <nav class="bg-white-800 p-4">
      <div class="max-w-7xl mx-auto">
        <div class="flex justify-center">
          <div class="flex space-x-4">
            <ul class="flex border-b">
              <!-- Navigation Links -->
              
              <li class="mr-1">
                <router-link to="/poolcreation" exact active-class="bg-blue-500 border-l border-t border-r rounded-t" class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold">Create Pool</router-link>
              </li>
              <li class="-mb-px mr-1">
                <router-link to="/" exact active-class="bg-blue-500 border-1 border-t border-r rounded-t" class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold">Pool Page</router-link>
              </li>
              <li class="mr-1">
                <router-link to="/notification" exact active-class="bg-blue-500 border-l border-t border-r rounded-t" class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold">Notifications</router-link>
              </li>
              <li class="mr-1">
                <router-link to="/login" exact active-class="bg-blue-500 border-l border-t border-r rounded-t" class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold">Logout</router-link>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: "NavBar",
    // Add any necessary logic here
  }
  </script>
  
  <style>
  /* Add any custom styles here */
  </style>
  