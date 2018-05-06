
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#booking-modal .booking-modal-contents").html("");
                $('#booking-modal').fadeTo(100, function() {
                    $(this).css("display", "inline-block");
                }).fadeTo(300, 1);
            },
            success: function (data) {
                $("#booking-modal .booking-modal-contents").html(data.html_form);
            },
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

                    $("#person-booking-table").html(data.html_booking_list);
                    $("#booking-modal").css("display", "none");
                    $(document).ready(function() {
                        var $myDiv = $('.js-delete-booking');
                        if ( $myDiv.length){
                            $(".empty").css("display", "none");
                        }
                    });
                    Swal();
                    console.log((form.context[2].value));
                    if ((form.context[2].value)>=1) {
                        console.log("queued");
                        queuedTab();
                        document.getElementById("booked-tab").className = "tablinks";
                        document.getElementById("queued-tab").className = "tablinks active";
                    }
                    else {
                        console.log("not queued");
                        bookedTab();
                        document.getElementById("queued-tab").className = "tablinks";
                        document.getElementById("booked-tab").className = "tablinks active";
                    }


                }
                else {
                    $("#booking-modal .booking-modal-contents").html(data.html_form);
                    Swal();
                    bookedTab();
                    document.getElementById("queued-tab").className = "tablinks";
                    document.getElementById("booked-tab").className = "tablinks active";
                }
            },
            complete: function (data) {

            }
        });
        return false;
    };

    // Create book
    $(".js-create-booking").click(loadForm);
    $("#booking-modal").on("submit", ".js-booking-create-form", saveForm);

    // Update book
    $("#person-booking-table").on("click", ".js-update-booking", loadForm);
    $("#booking-modal").on("submit", ".js-booking-update-form", saveForm);

      // Delete book
    $("#person-booking-table").on("click", ".js-delete-booking", loadForm);
    $("#booking-modal").on("submit", ".js-booking-delete-form", saveForm);



});

function Swal() {
    var span = document.createElement("span");
    span.innerHTML = " " + '</br>' + " Your changes has been saved";
    swal({
        title: "" + "Good job!" + "",
        content: span,
        icon: "success",
        buttons: false,
        timer: 4000,
    });
}


var modal = document.getElementById('booking-modal');
var modal2 = document.getElementById('modal-booking');

window.onclick = function(event) {
    if (event.target == modal || event.target == modal2 || event.target == close ) {
        $("#booking-modal").css("display", "none");
    }
};

bookedTab();

function bookedTab() {
    $( "tbody:contains('Queue')" ).css( "display", "None" );
    $( "tbody:contains('Queue')" ).prev().css( "display", "None" );
    $('tbody:not(:contains("Queue"))').css( "display", "contents" );
    $('tbody:not(:contains("Queue"))').prev().css( "display", "contents" );
}

function queuedTab() {
    $('tbody:not(:contains("Queue"))').css( "display", "None" );
    $('tbody:not(:contains("Queue"))').prev().css( "display", "None" );
    $( "tbody:contains('Queue')" ).css( "display", "contents" );
    $( "tbody:contains('Queue')" ).prev().css( "display", "contents" );
}

function openCity(event, type) {
    if(type=='Queued') {
        queuedTab();
    }
    if(type=='Booked'){
        bookedTab();
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    //document.getElementById(cityName).style.display = "block";
    event.currentTarget.className += " active";
}

