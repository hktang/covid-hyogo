<template>
  <div class="hello">
    <h1>{{ pageTitle }}</h1>
  </div>
</template>

<script>

async function init() {
    const { GoogleSpreadsheet } = require('google-spreadsheet');

    // spreadsheet key is the long id in the sheets URL
    const doc = new GoogleSpreadsheet('1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw');
    doc.useApiKey(process.env.GOOGLE_API_KEY);

    await doc.loadInfo();

    const sheet = doc.sheetsByIndex[0];
    console.log(sheet.title);
    console.log(sheet.rowCount);
}

init();

export default {
  name: 'Index',
  props: {
    pageTitle: String
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
