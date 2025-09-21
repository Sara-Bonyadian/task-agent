<script setup></script>

<template>
  <header class="p-4 border-b">
    <nav class="flex gap-4">
      <RouterLink to="/tasks">Tasks</RouterLink>
      <RouterLink to="/about">About</RouterLink>
    </nav>
  </header>

  <!-- This is required for route pages to show -->
  <main class="p-6">
    <RouterView />
  </main>
</template>

<style scoped></style>
