import { defineStore } from 'pinia';
import { useAuthStore } from './authStore';
import axios from 'axios';

export const useUsersStore = defineStore({
    id: 'user',
    state: () => ({
        userData: {},
        iti_data : [],
        user_iti : {},
    }),
    persist: true,
    actions: {
        async register(formData) {

        // try {
        //     this.userData = await axios.post('http://127.0.0.1:8000/api_d/v1/users/',formData)
        //     return  this.userData
        //   } catch (error) {
        //     // let the form component display the error
        //     console.log(error)
        //     return error
        //   }
        return null
        },

        async getUserPools(userid){
          const info  = await axios
            .get(`http://127.0.0.1:5200/get_userpools/${userid}`,{headers:{ "Content-Type":"application/json"}})

            console.log(info)
            return info

        },
        async getUserNoti(userid){
            const info  = await axios
              .get(`http://127.0.0.1:5200/get_notification/${userid}`,{headers:{ "Content-Type":"application/json"}})
  
              console.log(info)
              return info
  
          },

    }
});