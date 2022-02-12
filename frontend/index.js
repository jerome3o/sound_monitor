// TODO: need to insert the server addr.WebSocket
let server = "192.168.1.250";

function startPlotting(breakPoints, timeStep) {
  var ws = new WebSocket(`ws://${server}:8000/ws`);

  const dataLen = 200;
  const spectroX = [...Array(dataLen).keys()];
  let data = new Array(dataLen).fill(0);
  var spectrogramDataIn = new Array(dataLen).fill(
    Array(breakPoints.length).fill(0)
  );
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
      y: breakPoints.map((x) => `${x.toFixed(0)}Hz`),
      type: "heatmap",
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
}

fetch(`http://${server}:8000/settings`)
  .then((result) => result.json())
  .then((json) => {
    startPlotting(json.break_points, json.time_step);
  });
