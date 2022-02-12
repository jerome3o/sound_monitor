// TODO: need to insert the server address somehow.
var ws = new WebSocket("ws://192.168.1.250:8000/ws");

const dataLen = 200;
const spectroLen = 50;

const CHUNK = 1024 * 2;
const RATE = 44100;

const spectroX = [...Array(dataLen).keys()];

let data = new Array(dataLen).fill(0);
var spectrogramDataIn = new Array(dataLen).fill(Array(spectroLen).fill(0));
var spectrogramDataPlot = [[]];

let spectrogram = document.getElementById("spectrogram");

Plotly.newPlot("chart", [
  {
    y: data,
    type: "line",
  },
]);

Plotly.newPlot(spectrogram, [
  {
    z: spectrogramDataPlot,
    x: spectroX,
    type: "heatmap",
    yaxis: {
      type: "log",
      autorange: true,
    },
  },
]);

function transposeArray(array) {
  return array[0].map((_, i) => array.map((v) => v[i]));
}

setInterval(() => {
  spectrogramDataPlot = transposeArray(spectrogramDataIn);
  Plotly.restyle("spectrogram", "z", [spectrogramDataPlot]);
}, 200);

var c = -10;

ws.onmessage = function (event) {
  let _data = JSON.parse(event.data);

  data.push(_data.max_amplitude);
  data.shift();

  spectrogramDataIn.push(_data.spectra);
  spectrogramDataIn.shift();

  Plotly.update("chart", { y: [data] }, {}, [0]);
};
