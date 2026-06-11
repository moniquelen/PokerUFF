<template>
  <SessionCodeModal
    :show="showCodeModal"
    :code="sessionCode"
    @close="showCodeModal = false"
  />

  <UserNameModal
    :show="showUserNameModal"
    @confirm="setUsername"
  />

  <div class="session">
    <header class="header">
      <div class="logo">PokerUFF</div>
      <div class="session-title">
        {{ sessionName }}
      </div>
      <button class="share-btn">📤</button>
    </header>

    <div class="content">
      <button class="leave-btn" @click="leaveSession">
        Sair
      </button>
      <h1 class="title">Clique em um cartão para votar</h1>
      <div class="cards">
        <div
          v-for="value in cards"
          :key="value"
          class="card"
          @click="vote(value)"
        >
          {{ value }}
        </div>
      </div>

      <div class="participants">
        <h2>Participantes</h2>
        <div
          v-for="p in state.participants"
          :key="p"
          class="participant"
        >
          <span>{{ p }}</span>
          <span class="vote">
            <template v-if="!state.revealed">
              {{ state.votes[p] ? '✔' : '?' }}
            </template>
            <template v-else>
              {{ state.votes[p] ?? '-' }}
            </template>
          </span>
        </div>
      </div>

      <div v-if="isAdmin" class="sidebar">
        Sidebar ADM aq depois
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import SessionCodeModal from '@/components/SessionCodeModal.vue'
import UserNameModal from '@/components/UserNameModal.vue'

const route = useRoute()
const SESSION_CODE = route.params.code

const username = ref('')
const ws = ref(null)

const state = ref({
  participants: [],
  votes: {},
  revealed: false,
  admin: null,
  name: ''
})

const sessionName = ref('Sessão')
const isAdmin = ref(false)

const cards = [1, 2, 3, 5, 8, 13]

const showCodeModal = ref(false)
const sessionCode = ref('')
const showUserNameModal = ref(false)

function connect() {
  ws.value = new WebSocket(`ws://127.0.0.1:8000/ws/${SESSION_CODE}`)

  ws.value.onopen = () => {
    ws.value.send(JSON.stringify({
      type: 'sync'
    }))
  }

  ws.value.onmessage = (event) => {
    const msg = JSON.parse(event.data)

    if (msg.type === 'state') {
      state.value = msg.data

      sessionName.value = msg.data.name
      isAdmin.value = username.value === msg.data.admin
    }
  }
}

async function joinSession(name) {
  const res = await fetch('http://127.0.0.1:8000/session/join', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      code: SESSION_CODE,
      name
    })
  })

  if (!res.ok) {
    alert('Erro ao entrar na sessão')
    return
  }

  if (!ws.value) {
    connect()
  }
}

async function setUsername(name) {
  username.value = name

  showUserNameModal.value = false

  await joinSession(name)
}

function vote(value) {
  if (!ws.value) return

  ws.value.send(JSON.stringify({
    type: 'vote',
    user: username.value,
    value
  }))
}

function leaveSession() {
  if (ws.value) {
    ws.value.close()
    ws.value = null
  }
}

onMounted(async () => {
  const showSessionCodeModal =
    localStorage.getItem('showCodeModal') === 'true'

  if (showSessionCodeModal) {
    sessionCode.value = localStorage.getItem('sessionCode')
    showCodeModal.value = true
    localStorage.removeItem('showCodeModal')
    localStorage.removeItem('sessionCode')
  }

  const res = await fetch(`http://127.0.0.1:8000/session/${SESSION_CODE}`)

  if (!res.ok) {
    return
  }

  const data = await res.json()
  sessionName.value = data.name
  const pendingAdminName = localStorage.getItem('pendingAdminName')

  if (pendingAdminName) {
    username.value = pendingAdminName
    isAdmin.value = true

    localStorage.removeItem('pendingAdminName')
    await joinSession(pendingAdminName)

  } else {
    showUserNameModal.value = true
  }
})

onUnmounted(() => {
  if (ws.value) {
    ws.value.close()
  }
})
</script>

<style scoped>
.session {
  background: #121212;
  min-height: 100vh;
  color: white;
}

.header {
  height: 82px;
  background: #1E1E1E;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30px;
}

.logo {
  font-weight: 600;
}

.session-title {
  background: #121212;
  padding: 8px 16px;
  border-radius: 20px;
}

.content {
  padding: 120px 40px;
  position: relative;
}

.title {
  text-align: center;
  font-size: 28px;
  margin-bottom: 40px;
}

.cards {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-bottom: 60px;
}

.card {
  width: 120px;
  height: 180px;
  background: #565656;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  cursor: pointer;
  transition: 0.2s;
}

.card:hover {
  transform: scale(1.05);
}

.participants {
  max-width: 600px;
  margin: 0 auto;
}

.participant {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #1E1E1E;
}

.leave-btn {
  position: absolute;
  top: 20px;
  left: 20px;
  background: #565656;
  border: none;
  color: white;
  padding: 10px 15px;
  border-radius: 20px;
  cursor: pointer;
}

.sidebar {
  position: absolute;
  right: 20px;
  top: 120px;
  width: 250px;
  background: #1E1E1E;
  padding: 20px;
  border-radius: 12px;
}
</style>