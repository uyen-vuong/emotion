
var myPieChart = null;
// Function to update pie chart data
function updatePieChart(newData) {

    newData = get_default_format_pie_chart(newData);
    myPieChart.data = newData;
    myPieChart.update();
}

function get_default_format_pie_chart(data_list=null){

    if (data_list === null) data_list = [10, 10, 10, 10, 10, 10, 10, 10]
    // Sample data for the pie chart
    const data = {
        labels: labels,
        datasets: [{
            data: data_list, 
            // backgroundColor: ['#ff6384', '#36a2eb', '#ffce56']
        }]
    };
    return data;
}
function init_pie_chart(){
    data = get_default_format_pie_chart();
    // Configuration options for the pie chart
    const options = {
        responsive: true,
        maintainAspectRatio: false,
    };

    // Get the canvas element
    const ctx = document.getElementById('myPieChart').getContext('2d');

    // Create a new pie chart instance
    myPieChart = new Chart(ctx, {
        type: 'pie',
        data: data,
        options: options
    });
}