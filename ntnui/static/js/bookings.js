$(function () {

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#booking-modal .booking-modal-contents").html("");
        $('#booking-modal').fadeTo(100, 0.5, function() {
          $(this).css("display", "inline-block");
        }).fadeTo(300, 1);
      },
      success: function (data) {
        $("#booking-modal .booking-modal-contents").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#booking-table").html(data.html_booking_list);
          $("#booking-modal").css("display", "none");
        }
        else {
          $("#booking-modal .booking-modal-contents").html(data.html_form);
        }
      }
    });
    return false;
  };

  // Create book
  $(".js-create-booking").click(loadForm);
  $("#booking-modal").on("submit", ".js-booking-create-form", saveForm);

  // Update book
  $("#booking-table").on("click", ".js-update-booking", loadForm);
  $("#booking-modal").on("submit", ".js-booking-update-form", saveForm);

    // Delete book
  $("#booking-table").on("click", ".js-delete-booking", loadForm);
  $("#booking-modal").on("submit", ".js-booking-delete-form", saveForm);


});


var modal = document.getElementById('booking-modal');
var modal2 = document.getElementById('modal-booking');

window.onclick = function(event) {
  if (event.target == modal || event.target == modal2 || event.target == close ) {
    $("#booking-modal").css("display", "none");
  }
}


