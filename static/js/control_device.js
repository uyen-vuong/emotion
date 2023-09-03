$("#start").click(function () {
    let signal = { command: "START", lesson: lessonID };
    $.ajax({
      url: "/manager/control",
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
      contentType: "application/json",
      dataType: "json",
      data: JSON.stringify(signal),
      success: (response) => {
        console.log(response);
        alert("Successfully change state");
      },
      error: (err) => {
        console.log(err);
        alert("Something wrong, Please try again!");
      },
    });
});

$("#stop").click(function () {
    let signal = { command: "STOP", lesson: lessonID };
    $.ajax({
        url: "/manager/control",
        method: "POST",
        headers: { "X-CSRFToken": csrftoken },
        contentType: "application/json",
        dataType: "json",
        data: JSON.stringify(signal),
        success: (response) => {
        console.log(response);
        alert("Successfully change state");
        },
        error: (err) => {
        console.log(err);
        alert("Something wrong, Please try again!");
        },
    });
});