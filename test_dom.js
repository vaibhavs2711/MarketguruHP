const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('buy-cars.html', 'utf-8');
const dom = new JSDOM(html, { runScripts: "dangerously", resources: "usable" });

// Load cars-data.js
const carsDataJs = fs.readFileSync('cars-data.js', 'utf-8');
const scriptEl = dom.window.document.createElement("script");
scriptEl.textContent = carsDataJs;
dom.window.document.body.appendChild(scriptEl);

setTimeout(() => {
    try {
        console.log("Calling initPage...");
        dom.window.initPage();
        console.log("Rendered cars HTML length:", dom.window.document.getElementById('carList').innerHTML.length);
        console.log("Filtered cars length:", dom.window.filteredCars.length);
    } catch(e) {
        console.error("Runtime Error:", e);
    }
}, 1000);
