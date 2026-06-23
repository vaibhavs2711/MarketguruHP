const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('buy-cars.html', 'utf-8');
const dom = new JSDOM(html, { runScripts: "dangerously", url: "http://localhost/" });

const carsDataJs = fs.readFileSync('cars-data.js', 'utf-8');
// Mock localStorage
dom.window.localStorage = {
  getItem: () => null,
  setItem: () => {}
};
const scriptEl = dom.window.document.createElement("script");
scriptEl.textContent = carsDataJs;
dom.window.document.body.appendChild(scriptEl);

try {
    dom.window.initPage();
    console.log("Filtered cars:", dom.window.filteredCars.length);
} catch(e) {
    console.error("Error during initPage:", e);
}
