<template>
  <div class="footer">
    <h2>Wait, did you wash your hands?</h2>
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
        href="https://docs.google.com/spreadsheets/d/e/2PACX-1vTM9vP7fGowD3SKSGDGpIWBpbGHLclWW2TmbGyejLM5e3h9CwWvz9sP8a7I0C-F98bL6L-grr7bF6X5/pubhtml"
      >
        Google Spreadsheet</a
      >
      from
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
<style scoped>
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
