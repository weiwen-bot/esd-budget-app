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
        
        async accept_pool_request(payload){
            console.log(payload,"SDDS")
            const url = 'http://127.0.0.1:5100/accept_pool_request'
            // const url = 'http://localhost:8000/pm/accept_pool_request'
            try{
                const info = await axios
                .put(url,
                payload,
                {headers:{ "Content-Type":"application/json"}})
                console.log(info)
                return info
            }
            catch (error)
            {
                console.log(error)
            }
            
    },  

    async payment(payload){
        // {
        //     "pool_name": "pool_name",
        //     "UserID": 1,
        //     "PoolID": 1,
        //     "remaining": 100 * 100
        // }
        console.log(payload,"SDDS")
        try{
            const info = await axios
            .post(`http://127.0.0.1:5101/payment`,
            payload,
            {headers:{ "Content-Type":"application/json"}})
            console.log(info)
            return info
        }
        catch (error)
        {
            console.log(error)
        }
        
    },

    async refund(poolid){
        // {
        //     "pool_name": "pool_name",
        //     "UserID": 1,
        //     "PoolID": 1,
        //     "remaining": 100 * 100
        // }
        try{
            const info = await axios
            .post(`http://127.0.0.1:5101/refund/${poolid}`,
            {headers:{ "Content-Type":"application/json"}})
            console.log(info)
            return info
        }
        catch (error)
        {
            console.log(error)
        }
        
    },  
}
});