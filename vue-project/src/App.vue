<template>
  <div id="app">
    <div v-if="!nameEntered">
      <p v-if="nameError" style="color: red">{{ nameError }}</p>
      <input
        @keyup.enter="registerUser"
        @input="filterInput"
        v-model="name"
        placeholder="Enter your name"
      />
      <button @click="registerUser">Enter Chat</button>
    </div>
    <div v-else>
      <h1>Chat</h1>
      <div>
        <h2>Online Users</h2>
        <div id="online-users">
          <span v-for="user in onlineUsers" :key="user.sid">{{ user.name }}</span>
        </div>
        <hr />
      </div>
      <ul>
        <li
          v-for="(msg, index) in messages"
          :key="index"
          :class="{ 'my-message': isMyMessage(msg), 'other-message': !isMyMessage(msg) }"
        >
          <span class="name">{{ msg.name }} </span>
          <span class="msg-content" v-html="displayMessage(msg.message)"></span>
          <span class="msg-time">{{ msg.time }}</span>
        </li>
        <li v-if="botIsTyping" class="typing-indicator">Bot is typing...</li>
      </ul>
      <input
        v-model="message"
        placeholder="Write a message"
        @keyup.enter="sendMessage"
      />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<script>
import io from "socket.io-client";

export default {
  name: "App",
  data() {
    return {
      botIsTyping: false,
      message: "",
      messages: [],
      name: "",
      nameError: "",
      nameEntered: false,
      onlineUsers: [],
      socket: null,
    };
  },
  created() {
    this.connectToSocket();
  },
  methods: {
    connectToSocket() {
      this.socket = io("'http://chat-main-cont:5000'");
      this.socket.on("receive_message", (msg) => {
        this.messages.push(msg);
      });

      this.socket.on("users_online", (users) => {
        this.onlineUsers = users;
      });

      this.socket.on("registration_failed", (data) => {
        this.nameError = data.message;
        this.name = "";
        this.nameEntered = false;
      });

      this.socket.on("user_left", (name) => {
        this.onlineUsers = this.onlineUsers.filter(
          (user) => user.name !== name
        );
      });
      this.socket.on("bot_answer", () => {
        this.botIsTyping = false;
      });
    },
    displayMessage(message) {
      if (message.includes("```")) {
        let formattedMessage = message.replace(
          /```([^`]*)```/g,
          "<pre><code>$1</code></pre>"
        );
        return formattedMessage;
      }
      return message;
    },
    registerUser() {
      const firstLetterCharCode = this.name.charCodeAt(0);
      const isUppercase =
        firstLetterCharCode >= 65 && firstLetterCharCode <= 90;

      if (this.name.trim() && isUppercase && this.name.length >= 2) {
        this.socket.emit("register_user", this.name);
        this.nameEntered = true;
      } else {
        this.nameError = "You did not write a valid human name.";
      }
    },
    sendMessage() {
      if (this.name.trim() && this.message.trim()) {
        if (this.message.slice(0, 4) === "/ask") this.botIsTyping = true;
        let now = new Date();
        let formattedDate = now.toLocaleDateString("en-US", {
          year: "numeric",
          month: "long",
          day: "numeric",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
          hour12: false,
        });
        this.socket.emit("send_message", {
          message: this.message,
          name: this.name,
          time: formattedDate,
        });

        this.message = "";
      }
    },
    isMyMessage(msg) {
      return this.name === msg.name;
    },
    filterInput(event) {
      event.target.value = event.target.value.replace(/[^a-zA-Z_]/g, "");
    },
  },
};
</script>

<style scoped>
@import "./assets/style.css";
</style>
