<template>
  <div class="locale-changer">
    <label>{{ $t("displayLanguage") }}</label>
    <select v-model="$i18n.locale">
      <option v-for="(lang, i) in langs" :key="`Lang${i}`" :value="lang">{{
        $t("lang." + lang)
      }}</option>
    </select>
  </div>
</template>

<script>
export default {
  name: "LocaleChanger",
  data() {
    return { langs: ["en", "ja"] };
  }
};
</script>

<style scoped>
label {
  margin-right: 0.5rem;
}
</style>
