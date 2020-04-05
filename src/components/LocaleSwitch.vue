<template>
  <div class="locale-switch">
    <button
      v-for="(lang, key) in langs"
      :key="key"
      :value="key"
      class="btn"
      type="submit"
      @click="setLocale(key)"
    >
      {{ lang }}
    </button>
  </div>
</template>

<script>
import langs from "../langs";

export default {
  name: "LocaleSwitch",
  metaInfo() {
    return {
      title: this.$t("siteTagline"),
      titleTemplate: "COVID-19 in Hyogo: %s",
      htmlAttrs: {
        lang: this.currentLang
      }
    };
  },
  data() {
    return {
      langs: langs,
      currentLang: this.$i18n.locale
    };
  },
  methods: {
    setLocale: function(key) {
      this.$i18n.locale = key;
      this.currentLang = this.$i18n.locale;
    }
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
