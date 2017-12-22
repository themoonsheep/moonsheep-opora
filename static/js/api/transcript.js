// $(document).ready(function () {
//   console.log('aaa');
//   $('.page-range input[type=checkbox]').on('change', function (e) {
//     var checked = $(this).is(':checked');
//     $(this).parents('.page-range').find('.form-group').toggleClass('disabled');
//     $(this).parents('.page-range').find('input[type=text]').attr('disabled', checked);
//     $(this).parents('.page-range').find('input[type=text]').val('');
//   });
// });

// $(document).ready(function () {
//   $('form#taskForm').on('submit', function (e) {
//     e.preventDefault();
//     console.log($(this).serializeArray());
//     $.ajax({
//       type: 'POST',
//       url: $(this).attr('action'),
//       data: $(this).serialize(),
//       contentType: "application/json",
//       success: function (response) {
//         console.log(response);
//       },
//       error: function (cb) {
//         console.log(cb);
//       }
//     });
//   });
// });