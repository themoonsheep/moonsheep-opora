$(document).ready(function () {
  $('form#taskForm').on('submit', function (e) {
    e.preventDefault();
    console.log($(this).serializeArray());
    $.ajax({
      type: 'POST',
      // url: $(this).attr('action'),
      // data: $(this).serialize(),
      url: 'http://localhost:5000/api/taskrun',
      contentType: "application/json",
      data: JSON.stringify({
        task_id: 16,
        project_id: 1,
        info: {
          page: 14
        }
      }),
      success: function (response) {
        console.log(response);
      },
      error: function (cb) {
        console.log(cb);
      }
    });
  });
});