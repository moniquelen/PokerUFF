<template>
  <div
    v-if="show"
    class="overlay"
  >
    <div class="modal">
      <div class="text-container">
        <h1>
          Sessão criada com sucesso! 🎉
        </h1>

        <p>
          Compartilhe com a equipe o código abaixo:
        </p>
      </div>

      <div class="code-container">
        <span class="code">
          {{ code }}
        </span>

        <button
          class="copy-button"
          @click="copyCode"
        >
          <i class="mdi mdi-content-copy"></i>
          <span
            v-if="showTooltip"
            class="tooltip"
          >
            Código copiado
          </span>
        </button>
      </div>

      <div class="start-button">
        <PrimaryButton @click="$emit('close')">
          Iniciar
        </PrimaryButton>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PrimaryButton from '@/components/PrimaryButton.vue'

const props = defineProps({
  code: {
    type: String,
    required: true
  },
  show: {
    type: Boolean,
    required: true
  }
})

defineEmits(['close'])

const showTooltip = ref(false)

const copyCode = async () => {

  await navigator.clipboard.writeText(props.code)

  showTooltip.value = true

  setTimeout(() => {
    showTooltip.value = false
  }, 1500)

}
</script>

<style scoped>

.overlay{
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.8);
  display:flex;
  justify-content:center;
  align-items:center;
  z-index:1000;
}

.modal{
  width: 500px;
  background: #1E1E1E;
  border-radius: 26px;
  padding: 40px 50px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 22px;
}

h1{
  color: white;
  font-size: 28px;
  font-weight: 600;
  text-align: center;
  margin: 10px 0px;
}

p{
  color: white;
  font-size: 20px;
  text-align: center;
  margin-top: 0px;
  margin-bottom: 10px;
}

.code-container{
  width: 320px;
  height: 60px;
  background:#121212;
  border-radius:26px;
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:0 24px;
  position:relative;
}

.code{
  color:white;
  font-size:24px;
  font-weight:600;
  letter-spacing:4px;
}

.copy-button{
  background:none;
  border:none;
  cursor:pointer;
  position:relative;
}

.mdi{
  color:#565656;
  font-size:26px;
}

.tooltip{
  position:absolute;
  top:40px;
  right:-20px;
  background:#565656;
  color:white;
  padding:6px 10px;
  border-radius:12px;
  font-size:12px;
  white-space:nowrap;
}

.start-button{
  width: 180px;
  margin-top: 8px;
}

</style>