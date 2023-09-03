var old_fps = 0;
var old_student = 0;
var old_normal_student = 0;
var old_quality = 0;

function update_overview_value(data_update){
    fps = parseInt(data_update["fps"])
    student = data_update["student"]
    normal_student = data_update["normal_student"]
    lesson_quality = data_update["lesson_quality"]

    $("#fps").text(fps);
    $("#student").text(student);
    $("#normal_student").text(normal_student);
    $("#quality").text(lesson_quality);
    
    change_fps = parseInt(100 * (fps - old_fps) / Math.max(old_fps, 1));
    change_student =  parseInt(100* (student -old_student) / Math.max(1,old_student));
    change_normal_student =  parseInt(100 * (normal_student - old_normal_student) / Math.max(1, old_normal_student));
    change_lesson_quality =  parseInt(100 * (lesson_quality - old_quality) / Math.max(1,old_quality));
    
    list_update_id = ["fps_change", "student_change", "normal_student_change", "quality_change"]
    list_value_update = [change_fps, change_student, change_normal_student, change_lesson_quality]
    console.log(list_value_update)
    for (i = 0; i < 4; i ++){
      $(`#${list_update_id[i]}`).removeClass("text-success");
      $(`#${list_update_id[i]}`).removeClass("text-danger");
      if (list_value_update[i] <= 0){
        $(`#${list_update_id[i]}`).addClass("text-danger");
        $(`#${list_update_id[i]}`).text(`${list_value_update[i]}%`);
      }
      else{
        $(`#${list_update_id[i]}`).addClass("text-success");
        $(`#${list_update_id[i]}`).text(`+${list_value_update[i]}%`);
      }
    }
    old_fps = parseInt(fps);
    old_student = parseInt(student);
    old_normal_student = parseInt(normal_student)
    old_quality = parseInt(lesson_quality)
  }
// Create a WebSocket in JavaScript.
const chatSocket = new WebSocket("ws://" + window.location.host + "/ws/chat/" + roomName + "/");
console.log("Connect WS");
chatSocket.onmessage = function (e) {
   
    if (data["type"] === "text_message"){
        const data = JSON.parse(e.data);
        latest_data = data["text"];
        quantity = [];
        latest_quantity = [];
        labels.forEach((element) => {
            quantity.push(latest_data[element]);
            latest_quantity.push(latest_data[`latest_${element}`])
        })
        update_chart(labels, quantity); 
        updatePieChart(latest_quantity);
    }
    else if (data["type"] === "realtime_message"){
      const data = JSON.parse(e.data);
      // console.log(data)
      update_overview_value(data["message"]);
    }
    else{
        // update frame
        const receivedData = event.data; // Assuming it's an ArrayBuffer
				
				// Convert Blob to base64 string
				const reader = new FileReader();

				reader.onload = function(event) {
					// const base64String = event.target.result;
					const base64String = event.target.result.split(',')[1]; // Get the actual base64 data
					const imgElement = document.getElementById('imageElement'); // Replace with your img element
					imgElement.src = 'data:image/jpg;base64,' + base64String; // Set img src
				};
				reader.readAsDataURL(receivedData);
    }
}