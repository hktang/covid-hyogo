const axios = require("axios");
const fs = require("fs");

getDailyConfirmed(2).then(data => {
  writeFile("byDate.json", data);
});

getDailyConfirmed(3).then(data => {
  writeFile("byCity.json", data);
});

getDailyConfirmed(4).then(data => {
  writeFile("byAge.json", data);
});

getDailyConfirmed(5).then(data => {
  writeFile("byStatus.json", data);
});

getDailyConfirmed(6).then(data => {
  writeFile("byCluster.json", data);
});

getDailyConfirmed(7).then(data => {
  writeFile("summary.json", data);
});

function getDailyConfirmed(sheetId) {
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
  fs.writeFile("./src/data/" + fileName, JSON.stringify(data), function(err) {
    if (err) return console.log(err);
  });
}
