<template>
  <div class="locale-switch">
    <select v-model="$i18n.locale">
      <option v-for="(lang, i) in langs" :key="`Lang${i}`" :value="lang">{{
        lang
      }}</option>
    </select>
  </div>
</template>

<script>
export default {
  name: "LocaleSwitch",
  data() {
    return { langs: ["zh_CN", "en"] };
  }
};
</script>
