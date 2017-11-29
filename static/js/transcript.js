$(document).ready(function () {
  $('form#taskForm').on('submit', function (e) {
    e.preventDefault();
    console.log($(this).serializeArray());
    $.ajax({
      type: 'POST',
      url: $(this).attr('action'),
      data: $(this).serialize(),
      contentType: "application/json",
      success: function (response) {
        console.log(response);
      },
      error: function (cb) {
        console.log(cb);
      }
    });
  });
});