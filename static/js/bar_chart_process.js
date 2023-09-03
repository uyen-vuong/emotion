var myChart = null;
function covert_ISO_to_date(ISO_date_str) {
    date = new Date(ISO_date_str);
    year = date.getFullYear();
    month = date.getMonth() + 1;
    dt = date.getDate();
    if (dt < 10) {
      dt = "0" + dt;
    }
    if (month < 10) {
      month = "0" + month;
    }
    return year + "-" + month + "-" + dt;
  }
function get_default_format_data(labels, data_list) {
  const data = {
    labels: labels,
    datasets: [
      {
        axis: "y",
        label: "Distribution Emotion Data",
        data: data_list,
        barPercentage: 0.5,
        barThickness: 20,
        maxBarThickness: 25,
        fill: true,
        backgroundColor: ["#e67e22"],
        borderColor: ["#e67e22"],
        borderWidth: 1,
      },
    ],
  };
  return data;
}
function get_default_chart() {
  labels = [
    "neutral",
    "happiness",
    "surprise",
    "sadness",
    "anger",
    "disgust",
    "fear",
    "contempt",
  ];
  const data = {
    labels: labels,
    datasets: [
      {
        axis: "y",
        label: "Distribution Emotion Data",
        data: [0, 0, 0, 0, 0, 0, 0, 0],
        barPercentage: 0.5,
        barThickness: 20,
        maxBarThickness: 25,
        fill: true,
        backgroundColor: ["#e67e22"],
        borderColor: ["#e67e22"],
        borderWidth: 1,
      },
    ],
  };
  return data;
}
function update_chart(labels, data) {
  data_update = get_default_format_data(labels, data);
  myChart.data = data_update;
  myChart.update();
}

function init_bar_chart(){
   // load workspace
   data = get_default_chart();
   const config = {
     type: "bar",
     data,
     options: {
       indexAxis: "y",
     },
   };
   myChart = new Chart(document.getElementById("analysis-chart"), config);
   get_info_chart();
}