<script setup>
import {ref, onMounted} from "vue";
import {TaskService} from "@/lib/api"

const tasks=ref([]);
const loading=ref(true);
const error =ref("");
onMounted(async () => {
  try {
    tasks.value = await TaskService.list(); // GET /tasks
  } catch (e) {
    error.value = e?.message || "Failed to load tasks";
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="p-6">
    <h1 class="text-2xl font-semibold mb-4">Tasks</h1>

    <p v-if="loading">Loading…</p>
    <p v-else-if="error" class="text-red-600">Error: {{ error }}</p>
    <p v-else-if="!tasks.length">No tasks yet.</p>

    <ul v-else class="space-y-2">
      <li v-for="t in tasks" :key="t.id" class="p-3 rounded border">
        <span class="font-medium">{{ t.title }}</span>
        <span v-if="t.done" class="ml-2 text-xs">✔</span>
      </li>
    </ul>
  </div>
</template>