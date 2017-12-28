$(document).ready(function () {
  console.log('aaa');
  $('.page-range input[type=checkbox]').on('change', function (e) {
    var checked = $(this).is(':checked');
    $(this).parents('.page-range').find('.form-group').toggleClass('disabled');
    $(this).parents('.page-range').find('input[type=text]').attr('disabled', checked);
    $(this).parents('.page-range').find('input[type=text]').val('');
  });
});
