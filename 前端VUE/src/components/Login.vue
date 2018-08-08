<template>
    <div>
      <h1>用户登录</h1>
      <input type="text" placeholder="用户名" v-model="username">
      <input type="text" placeholder="密码" v-model="password">
      <input type="button" value="提交" @click="doLogin">
      <a v-on:click="doLogin">click me</a>
    </div>
</template>

<script>
    export default {
        name: "Login",
      data(){
          return {
            username:'',
            password:'',
          }
      },
      mounted(){
          this.doLogin();
      },
      methods:{
          doLogin:function () {
            // 向后台发送ajax请求
            this.$axios.request({
              url:'http://127.0.0.1:8000/api/v1/auth/',
              method:'POST',
              data:{
                user:this.username,
                pwd:this.password,

              },
              headers:{
                // 'Content-Type':'application/json'
              },
              responseType:'json'
            }).then(function (arg) {
              // 成功之后
              console.log(arg);

            }).catch(function (arg) {

            })

          }
      }
    }
</script>

<style scoped>

</style>
