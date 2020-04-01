<template>
  <div class="footer">
    <div class="share">
      <h2>Share this page</h2>
      <AddThis public-id="ra-5e7cafe6d8afe9ba" />
    </div>
    <img
      alt="Pathogen resistance"
      class="webcomic"
      src="https://imgs.xkcd.com/comics/pathogen_resistance_2x.png"
    />
    <h2 class="references">Data sources and references</h2>

    <p>
      Inspired by
      <a href="https://blog.datawrapper.de/coronaviruscharts/">
        17 responsible live visualizations about the coronavirus</a
      >
    </p>
    <p>
      Data available as
      <a
        href="https://docs.google.com/spreadsheets/d/1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw/edit?usp=sharing"
      >
        Google Spreadsheet</a
      >
      , compiled from
      <a href="https://web.pref.hyogo.lg.jp/kk03/corona_hasseijyokyo.html">
        新型コロナウイルスに感染した患者の発生状況</a
      >, Hyogo Prefectural Government
    </p>
    <p>
      Population data from
      <a href="https://ja.wikipedia.org/wiki/%E5%85%B5%E5%BA%AB%E7%9C%8C"
        >Wikipedia</a
      >.
    </p>
    <p>Webcomic from <a href="https://xkcd.com/2287/">XKCD</a></p>
    <p>
      View project on
      <a href="https://github.com/hktang/covid-hyogo/">Github</a>
    </p>
  </div>
</template>
<script>
import AddThis from "vue-simple-addthis-share";

export default {
  name: "Footer",
  components: {
    AddThis
  }
};
</script>
<style scoped>
.share {
  padding: 10px 0 30px;
  margin-bottom: 40px;
}
.references {
  margin-top: 40px;
}
@media only screen and (max-width: 800px) {
  .webcomic {
    width: 100vw;
  }
}

@media only screen and (min-width: 800px) {
  .webcomic {
    width: 60vw;
  }
}
</style>
