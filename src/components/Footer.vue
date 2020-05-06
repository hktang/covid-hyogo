<template>
  <div class="footer">
    <i18n path="footer.github.text" tag="p">
      <template v-slot:0>
        <a :href="urls.github">{{ $t("footer.github.github") }}</a>
      </template>
    </i18n>

    <i18n path="announcement.title" tag="p">
      <template v-slot:0>
        <a :href="urls.translate">{{ $t("announcement.platform") }}</a>
      </template>
    </i18n>

    <h2 class="references">{{ $t("thanks.text") }}</h2>
    <p>
      {{ $t("thanks.developers") }}
      <a href="https://github.com/akiya64">akiya64</a>
    </p>
    <p>
      {{ $t("thanks.translators") }}
      Adhura Husna, <a href="https://github.com/akiya64">akiya64</a>, Christmas
      Uchiyama, Jeeban Panthi, Linda Anne Stevenson, Mary Antonette Ramos,
      Nafesa Ismail
    </p>

    <div class="share">
      <h2>{{ $t("footer.share") }}</h2>
      <AddThis public-id="ra-5e7cafe6d8afe9ba" />
    </div>

    <h2 class="celebration">{{ $t("footer.caption") }}</h2>

    <img
      v-if="$i18n.locale != 'zh'"
      alt="Pathogen resistance"
      class="webcomic"
      src="https://imgs.xkcd.com/comics/pathogen_resistance_2x.png"
    />
    <img
      v-else
      alt="Pathogen resistance"
      class="webcomic"
      src="https://xkcd.in/resources/compiled_cn/09e2f4a69c20330cff3de498e6a0aada.jpg"
    />

    <h2 class="references">{{ $t("footer.references") }}</h2>

    <i18n path="footer.inspiredBy.text" tag="p">
      <template v-slot:0>
        <a :href="urls.blog">{{ $t("footer.inspiredBy.blogTitle") }}</a>
      </template>
    </i18n>

    <i18n path="footer.dataFrom.text" tag="p">
      <template v-slot:0>
        <a :href="urls.spreadsheet">{{ $t("footer.dataFrom.spreadsheet") }}</a>
      </template>
      <template v-slot:1>
        <a :href="urls.hyogo">{{ $t("footer.dataFrom.hyogoPage") }}</a>
      </template>
    </i18n>

    <i18n path="footer.population.text" tag="p">
      <template v-slot:0>
        <a :href="urls.wikipedia">{{ $t("footer.population.wikipedia") }}</a>
      </template>
    </i18n>

    <i18n path="footer.xkcd.text" tag="p">
      <template v-slot:0>
        <a :href="urls.xkcd">{{ $t("footer.xkcd.xkcd") }}</a>
      </template>
    </i18n>

    <cookie-law />
  </div>
</template>
<script>
import AddThis from "vue-simple-addthis-share";
import CookieLaw from "vue-cookie-law";

export default {
  name: "Footer",
  components: {
    AddThis,
    CookieLaw
  },
  data: () => ({
    urls: {
      translate: "https://www.transifex.com/covid-19-hyogo/covid-19-in-hyogo/",
      blog: "https://blog.datawrapper.de/coronaviruscharts/",
      spreadsheet:
        "https://docs.google.com/spreadsheets/d/1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw/edit?usp=sharing",
      hyogo: "https://web.pref.hyogo.lg.jp/kk03/corona_hasseijyokyo.html",
      wikipedia: "https://ja.wikipedia.org/wiki/%E5%85%B5%E5%BA%AB%E7%9C%8C",
      xkcd: "https://xkcd.com/2287/",
      github: "https://github.com/hktang/covid-hyogo/"
    }
  })
};
</script>
<style scoped>
.share {
  padding: 10px 0 30px;
  margin-bottom: 40px;
}
.celebration {
  margin-bottom: 30px;
}
.references {
  margin-top: 40px;
}
@media only screen and (max-width: 800px) {
  .webcomic {
    width: 95vw;
  }
}

@media only screen and (min-width: 800px) {
  .webcomic {
    width: 60vw;
  }
}
</style>
