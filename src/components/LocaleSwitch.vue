<template>
  <div class="locale-switch">
    <button
      v-for="(lang, key) in langs"
      :key="key"
      :value="key"
      class="btn"
      type="submit"
      @click="$i18n.locale = key"
    >
      {{ lang }}
    </button>
  </div>
</template>

<script>
export default {
  name: "LocaleSwitch",
  data() {
    return { langs: this.$t("lang") };
  }
};
</script>

<style scoped>
.btn {
  background: none;
  border: none;
  text-decoration: underline;
  cursor: pointer;
  font-size: 14px;
}
.btn:hover {
  color: #42b983;
}
.locale-switch {
  background: #fafafa;
  padding: 6px;
  margin: 0 0 40px;
}
</style>
