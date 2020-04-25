const axios = require("axios");
const fs = require("fs");

const files = {
  2: "byDate.json",
  3: "byCity.json",
  4: "byAge.json",
  5: "byStatus.json",
  6: "byCluster.json",
  7: "summary.json"
};

for (const [key, value] of Object.entries(files)) {
  getSheet(key).then(data => {
    writeFile(value, data);
  });
}

function getSheet(sheetId) {
  return axios
    .get(
      "https://spreadsheets.google.com/feeds/cells/" +
        "1B0aXcDc2IOkKRcWqoQzVsswoJ-rd5hXp8DYgT9KyqDw/" +
        sheetId +
        "/public/basic?alt=json"
    )
    .then(response => {
      return response.data;
    })
    .catch(error => {
      console.log(error);
    });
}

function writeFile(fileName, data) {
  let chartData = null;

  switch (data.feed.title.$t.substring(0, 1)) {
    case "2":
      chartData = getDataSetsByDate(data);
      break;
    case "3":
      chartData = getDataSetsByCity(data);
      break;
    case "4":
      chartData = getDataSetsByAge(data);
      break;
    case "5":
      chartData = getDataSetsByStatus(data);
      break;
    case "6":
      chartData = getDataSetsByCluster(data);
      break;
    case "7":
      chartData = getDataSetsSummary(data);
      break;
    default:
      chartData = data;
      break;
  }

  fs.writeFile(
    "./src/data/" + fileName,
    JSON.stringify(chartData, null, 1),
    function(err) {
      if (err) return console.log(err);
    }
  );
}

function getDataSetsByDate(data) {
  let dataSet = {};

  const dateColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "A"
  );
  const femaleColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "B"
  );
  const maleColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "C"
  );

  dateColumn.shift();
  dataSet.dateLabels = dateColumn.map(value => value["content"]["$t"]);

  femaleColumn.shift();
  dataSet.female = femaleColumn.map(value => value["content"]["$t"]);

  maleColumn.shift();
  dataSet.male = maleColumn.map(value => value["content"]["$t"]);

  return dataSet;
}

function getDataSetsByCity(data) {
  let dataSet = {};
  cities = [];

  const latColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "A"
  );
  const lngColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "B"
  );
  const cityColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "C"
  );
  const casesColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "D"
  );

  for (let i = 1; i < latColumn.length; i++) {
    cities.push({
      lat: Number(latColumn[i]["content"]["$t"]),
      lng: Number(lngColumn[i]["content"]["$t"]),
      name: cityColumn[i]["content"]["$t"],
      cases: Number(casesColumn[i]["content"]["$t"])
    });
  }

  dataSet.cities = cities;

  return dataSet;
}

function getDataSetsByAge(data) {
  let dataSet = {};

  const labelColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "A"
  );
  const confirmedColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "B"
  );
  const deathsColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "C"
  );

  labelColumn.shift();
  dataSet.ageLabels = labelColumn.map(value => value["content"]["$t"]);

  confirmedColumn.shift();
  dataSet.confirmed = confirmedColumn.map(value => value["content"]["$t"]);

  deathsColumn.shift();
  dataSet.deaths = deathsColumn.map(value => value["content"]["$t"]);

  return dataSet;
}

function getDataSetsByStatus(data) {
  return data;
}

function getDataSetsByCluster(data) {
  return data;
}

function getDataSetsSummary(data) {
  let dataSet = {};
  dataSet.updated = data.feed.updated.$t;
  dataSet.totalTested = getCell(data, "B1");
  dataSet.totalConfirmed = getCell(data, "B2");
  dataSet.totalDeaths = getCell(data, "B3");
  dataSet.population = getCell(data, "B4");

  return dataSet;
}

function getCell(responseData, cell) {
  let data = responseData.feed.entry.filter(entry => {
    return entry["title"]["$t"] === cell;
  });

  return Number(data[0]["content"]["$t"]);
}
