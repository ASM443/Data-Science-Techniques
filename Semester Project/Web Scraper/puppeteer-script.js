const puppeteer = require('puppeteer');
const fs = require('fs');

async function getEstimatedTravelTime(page, stop0, stop1) {
  try {
    // Click the button with id 'divOKButton'
    //await page.click('#divOKButton');

    await page.evaluate(() => {
        document.querySelector('#stop-0').value = '';
        document.querySelector('#stop-1').value = '';
      });

    // Enter text into the input elements with ids 'stop-0' and 'stop-1'
    await page.type('#stop-0', stop0);
    await page.type('#stop-1', stop1);

    // Call the 'solve()' function instead of clicking the button
     await page.evaluate(() => {
       solve();
       
     });

    // Wait for some time to capture the console output and the page content
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Get the entire HTML content of the page
    const htmlContent = await page.content();

    // Search for the string "Estimated Travel Time: " and extract the number after
    const regex = /Estimated Travel Time: (\d+)/;
    const match = htmlContent.match(regex);

    if (match) {
      console.log(stop0, " - ", stop1, ": ", match[1]);
      return match[1];
    } else {
      console.log(stop0, " - ", stop1, ": ",'not found');
      return null;
    }
  } catch (error) {
    console.error(error.message);
  }
}

(async () => {
  try {
    const browser = await puppeteer.launch({ headless: false });
    const page = await browser.newPage();

    // Capture console events from the page
    // page.on('console', msg => {
    //   console.log('Browser console output:', msg.text());
    // });

    await page.goto('https://maps.umd.edu/map/');

    // Wait for 2 seconds (2000 milliseconds) at the start
    await new Promise(resolve => setTimeout(resolve, 6000));

    const stops = ['TYD', 'SKN', 'SQH', 'HBK', 'ASY', 'KEY', 'JMZ', 'ESJ', 'TLF',
     'TWS', 'PAC', 'HJP', 'KNI', 'PLS', 'LEF', 'PHY',
    'MTH', 'CHE', 'ANS', 'ATL', 'IRB', 'SHM', 'TLFB', 'ARC', 'SYM',
    'QAN', 'ESJB', 'ARM', 'CHM', 'ASYA', 'IPT', 'KEB', 'AJC', 'EGR',
    'BPS', 'COL', 'BRB', 'SPH', 'BLD', 'MCB', 'VMH', 'CCC', 'VMHH',
    'SOM', 'BA', 'DCC', 'LEFE', 'CSI', 'JMP', 'EDU', 'MMH', 'SPP',
    'MTHB', 'EGL', 'AVW', 'JMZA', 'GEO', 'CHI', 'PFR', 'PHYB', 'ERCBE',
    'PKT', 'SPHA', 'YDHA', 'YDHF', 'JUL', 'HBKJ', 'HBKH', 'HBKG',
    'TWSB', 'TWSA', 'ERC', 'ERCB', 'MCKA', 'MMHB', 'CEN', 'PACA',
    'PSC', 'BPSB', 'SPHB', 'EDUB'];

    const graph = {};

    

    for (let i = 0; i < stops.length; i++) {
      for (let j = i + 1; j < stops.length; j++) {
        const stop0 = stops[i];
        const stop1 = stops[j];

        const travelTime = await getEstimatedTravelTime(page, stop0, stop1);
        if (travelTime !== null) {
          const key = `${stop0}-${stop1}`;
          graph[key] = travelTime;
        }
      }
    }
    
    console.log('Graph:', graph);
    fs.writeFileSync('graph2.json', JSON.stringify(graph, null, 2));
    // await browser.close();

  } catch (error) {
    console.error(error.message);
  }
})();
