<template>
  <div class="footer">
    <div class="share">
      <h2>Share this page</h2>
      <AddThis public-id="ra-5e7cafe6d8afe9ba" />
    </div>
    <h2>Wait, did you wash your hands properly?</h2>
    <img
      alt="Often missed"
      class="hands"
      src="../assets/handwashing-missed.png"
    />
    <h2>Data sources and references</h2>

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
    <p>
      Hands graphic by Taylor LJ via
      <a
        href="https://flowingdata.com/2020/02/18/most-often-missed-areas-while-washing-hands/"
        >Flowing Data</a
      >
    </p>
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
  background-color: #f3f3f3;
  padding: 10px 0 30px;
  margin-bottom: 60px;
}
@media only screen and (max-width: 800px) {
  .hands {
    width: 70vw;
  }
}

@media only screen and (min-width: 800px) {
  .hands {
    width: 40vw;
  }
}
</style>
