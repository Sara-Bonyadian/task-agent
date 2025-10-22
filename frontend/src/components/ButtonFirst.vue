<script setup>
const props = defineProps({
  label: { type: String, required: true },
  type: { type: String, default: "button" },
});
</script>

<template>
  <button
    :type="type"
    class="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 transition"
  >
    {{ label }}
  </button>
</template>
