<template>
  <div>
    <!-- 添加用户按钮 -->
    <button
      @click="showAddUserForm = true"
      class="bg-green-500 text-white px-4 py-2 rounded mt-4"
    >
      Add user
    </button>

    <!-- 用户列表 -->
    <table class="min-w-full bg-white">
      <thead>
        <tr >
          <th class="py-2 px-4 border-b">id</th>
          <th class="py-2 px-4 border-b">name</th>
          <th class="py-2 px-4 border-b">gender</th>
          <th class="py-2 px-4 border-b">edit</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in paginatedUsers" :key="user.uid">
          <td class="py-2 px-4 border-b">{{ user.uid }}</td>
          <td class="py-2 px-4 border-b">{{ user.name }}</td>
          <td class="py-2 px-4 border-b">{{ user.gender }}</td>
          <td class="py-2 px-4 border-b">
            <button
              @click="editUser(user)"
              class="bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
            >
            EDIT
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="flex justify-start items-center mt-4">
      <button
        @click="prevPage"
        :disabled="currentPage === 1"
        class="bg-gray-300 text-gray-700 px-3 py-1 rounded disabled:opacity-50"
      >
        <
      </button>
      <div class="flex space-x-2 mx-4">
        <button
          v-for="page in totalPages"
          :key="page"
          @click="goToPage(page)"
          :class="['px-3 py-1 rounded', { 'bg-blue-500 text-white': page === currentPage, 'bg-gray-300 text-gray-700': page !== currentPage }]"
        >
          {{ page }}
        </button>
      </div>
      <button
        @click="nextPage"
        :disabled="currentPage === totalPages"
        class="bg-gray-300 text-gray-700 px-3 py-1 rounded disabled:opacity-50"
      >
        >
      </button>
    </div>

    <!-- 添加用户表单||修改用户表单 -->
    <div v-if="showAddUserForm || showEditUserForm" class="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75">
      <div class="bg-white p-6 rounded shadow-md">
        <h2 class="text-xl mb-4">{{ showAddUserForm ? 'Add user':'Edit user' }}</h2>
        <form @submit.prevent="showAddUserForm ? addUser() : updateUser()">
          <div class="mb-4 flex items-center">
            <label class="w-1/4 block text-gray-700" >Name:</label>
            <input v-model="currentUser.name" type="text" class="w-3/4 px-3 py-2 border rounded" required>
          </div>
          <div class="mb-4 flex items-center">
            <label class="w-1/4 block text-gray-700">Gender:</label>
            <select v-model="currentUser.gender" class="w-3/4 px-3 py-2 border rounded" required>
              <option value="female">female</option>
              <option value="male">male</option>
              <option value="others">others</option>
            </select >
          </div>
          <div class="flex justify-end">
            <button type="button" @click="cancelForm" class="bg-gray-500 text-white px-4 py-2 rounded mr-2">cancel</button>
            <button type="submit" class="bg-blue-500 text-white px-4 py-2 rounded">confirm</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {

      currentPage: 1,
      pageSize: 5,
      showAddUserForm: false,
      showEditUserForm: false,
      currentUser: {
        uid: '',
        name: '',
        gender: ''
      },
      paginatedData: [
      ]
    };
  },
  computed: {
    //计算总页数
    totalPages() {
      return Math.ceil(this.paginatedData.length / this.pageSize);
    },
    //计算当前页的数据
    paginatedUsers() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.paginatedData.slice(start, end);
    }
  },
  methods: {
    //点击跳转页
    goToPage(page) {
      this.currentPage = page;
    },
    //下一页
    nextPage() {
      this.currentPage += 1;
    },
    //上一页
    prevPage() {
      this.currentPage -= 1;
    },
    //取消按钮
    cancelForm() {
      this.showAddUserForm = false;
      this.showEditUserForm = false;
    },
    //添加用户
    addUser() {
    axios.post('http://api.localhost.com:3030/add_user', this.currentUser)
      .then(response => {
        console.log(response.data);
        this.getUsers();
        this.cancelForm();
      })
      .catch(error => {
        console.error(error);
      });

    },
    // 获取用户列表
    getUsers(){
      axios.get('http://api.localhost.com:3030/get_user_list')
        .then(response => {
          console.log(response.data.data);
          this.paginatedData = response.data.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    //编辑用户
    editUser(user) {
      this.currentUser = { ...user };
      this.showEditUserForm = true;
    },
    //更新用户
    updateUser() {

      axios.put(`http://api.localhost.com:3030/edit_user/${this.currentUser.uid}`, this.currentUser)
        .then(response => {
          console.log(response.data);
          this.getUsers();
          this.cancelForm();
        })
        .catch(error => {
          console.error(error);
        });
    }
  },

  //组件挂载时获取用户列表
  mounted(){
      this.getUsers();
    }

};
</script>

<style scoped>
/* 添加样式 */
</style>
