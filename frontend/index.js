// TODO: need to insert the server address somehow.
var ws = new WebSocket("ws://localhost:8000/ws");

const dataLen = 200;
let data = new Array(dataLen).fill(0);

Plotly.newPlot("chart", [
  {
    y: data,
    type: "line",
  },
]);

ws.onmessage = function (event) {
  data.push(parseFloat(event.data) / 2 ** 32);
  data.shift();
  //   console.log(data);
  Plotly.update("chart", { y: [data] }, {}, [0]);
};
