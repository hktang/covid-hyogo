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

  fs.writeFile("./src/data/" + fileName, JSON.stringify(chartData), function(
    err
  ) {
    if (err) return console.log(err);
  });
}

function getDataSetsByDate(data) {
  let dataSet = {};

  const dateColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "A"
  );

  dataSet.dateLabels = filterColumn(dateColumn);

  const femaleColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "B"
  );

  dataSet.female = filterColumn(femaleColumn);

  const maleColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "C"
  );

  dataSet.male = filterColumn(maleColumn);

  const totalColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "D"
  );

  dataSet.total = filterColumn(totalColumn);

  const sevenDayMovingAverageColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "E"
  );

  dataSet.sevenDayMovingAverage = filterColumn(sevenDayMovingAverageColumn);

  return dataSet;
}

function getDataSetsByCity(data) {
  let dataSet = {};
  let cities = [];

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

  dataSet.ageLabels = filterColumn(labelColumn);

  const confirmedColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "B"
  );

  dataSet.confirmed = filterColumn(confirmedColumn);

  const deathsColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "C"
  );

  dataSet.deaths = filterColumn(deathsColumn);

  return dataSet;
}

function getDataSetsByStatus(data) {
  let dataSet = {};

  const dateColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "A"
  );

  dataSet.dateLabels = filterColumn(dateColumn);

  const totalTestedColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "B"
  );

  dataSet.totalTested = filterColumn(totalTestedColumn);

  const confirmedColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "C"
  );

  dataSet.confirmed = filterColumn(confirmedColumn);

  const hospitalizedColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "D"
  );

  dataSet.hospitalized = filterColumn(hospitalizedColumn);

  const nonSevereCasesColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "E"
  );

  dataSet.nonSevereCases = filterColumn(nonSevereCasesColumn);

  const severeCasesColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "F"
  );

  dataSet.severeCases = filterColumn(severeCasesColumn);

  const deathsColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "G"
  );

  dataSet.deaths = filterColumn(deathsColumn);

  const dischargedColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "H"
  );

  dataSet.discharged = filterColumn(dischargedColumn);

  const totalBedsColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "I"
  );

  dataSet.totalBeds = filterColumnWithNaN(totalBedsColumn);

  const hospitalBedsColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "J"
  );

  dataSet.hospitalBeds = filterColumnWithNaN(hospitalBedsColumn);

  const otherFacilitiesColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "K"
  );

  dataSet.otherBeds = filterColumnWithNaN(otherFacilitiesColumn);

  return dataSet;
}

function getDataSetsByCluster(data) {
  let dataSet = {};

  const caseNumberColumn = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(0, 1) == "B"
  );

  dataSet.caseNumber = filterColumn(caseNumberColumn);

  const clusterRow = data.feed.entry.filter(
    entry => entry["title"]["$t"].substring(1) == "1"
  );

  dataSet.clusters = {};

  for (let i = 2; i < clusterRow.length; i++) {
    const item = clusterRow[i];
    const key = item.title.$t.substring(0, 1);
    dataSet.clusters[key] = item.content.$t;
  }

  const cases = data.feed.entry.filter(entry => {
    return (
      entry["content"]["$t"].trim() === "〇" ||
      entry["content"]["$t"].trim() === "○"
    );
  });

  dataSet.caseVsCluster = [];

  for (let i = 0; i < cases.length; i++) {
    const item = cases[i];
    dataSet.caseVsCluster.push(item.title.$t);
  }

  return dataSet;
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

function filterColumn(column) {
  column.shift();
  return column.map(value =>
    isNaN(value["content"]["$t"])
      ? value["content"]["$t"]
      : Number(value["content"]["$t"])
  );
}

function filterColumnWithNaN(column) {
  column.shift();
  return column.map(value =>
    isNaN(value["content"]["$t"]) ? null : Number(value["content"]["$t"])
  );
}
