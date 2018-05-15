// Script for creating bookings

// Activate booked tab on page load
bookedTab();

// Ajax functions to load and save bookings
$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: "get",
            dataType: "json",
            beforeSend: function (data) {
                $("#booking-modal .booking-modal-contents").html("");
                $("#booking-modal").fadeTo(100, function() {
                    $(this).css("display", "inline-block");
                }).fadeTo(300, 1);
            },
            success: function (data) {
                $("#booking-modal .booking-modal-contents").html(data.html_form);
            },
        });
    };

    var saveForm = function (event) {
        var form = $(this);
        var newForm = form.serializeArray();
        if (event.target.className == "js-booking-update-form"){
            var startTime = document.getElementById("startInput").value.toString();
            var endTime = document.getElementById("endInput").value.toString();
            var dates = document.getElementById("date").value.toString();
            newForm.forEach(function (item) {
                if (item.name === "start"){
                    item.value = dates + " " + startTime;
                } else if (item.name === "end"){
                    item.value = dates + " " + endTime;
                }
            });
        }
        $.ajax({
            url: form.attr("action"),
            data: newForm,
            type: form.attr("method"),
            dataType: "json",
            success: function (data) {
                if (data.form_is_valid) {
                    if ($("#person-booking-table").length) {
                        $("#person-booking-table").html(data.html_booking_list);
                    }
                    if ($("#manage-booking-table").length) {
                        $("#manage-booking-table").html(data.html_all_booking_list);
                    }
                    $("#booking-modal").css("display", "none");
                    $(document).ready(function() {
                        var $myDiv = $('.js-delete-booking');
                        if ( $myDiv.length){
                            $(".empty").css("display", "none");
                        }
                    });
                    Swal();
                    // Check if deleted booking is queued
                    if (event.target.className == "js-booking-delete-form") {
                        if (form[0].id > 0) {
                            queuedTab();
                            document.getElementById("booked-tab").className = "tablinks";
                            document.getElementById("queued-tab").className = "tablinks active";
                        } else {
                            bookedTab();
                            document.getElementById("queued-tab").className = "tablinks";
                            document.getElementById("booked-tab").className = "tablinks active";
                        }
                    } else {
                        if ((form.context[3].value)>0) {
                            queuedTab();
                            document.getElementById("booked-tab").className = "tablinks";
                            document.getElementById("queued-tab").className = "tablinks active";
                        } else {
                            bookedTab();
                            document.getElementById("queued-tab").className = "tablinks";
                            document.getElementById("booked-tab").className = "tablinks active";
                        }
                    }
                } else {
                    $("#booking-modal .booking-modal-contents").html(data.html_form);
                    Swal();
                    bookedTab();
                    document.getElementById("queued-tab").className = "tablinks";
                    document.getElementById("booked-tab").className = "tablinks active";
                }
            }
        });
        return false;
    };

    // Create book
    $(".js-create-booking").click(loadForm);
    $("#booking-modal").on("submit", ".js-booking-create-form", saveForm);

    // Update book
    $("#person-booking-table").on("click", ".js-update-booking", loadForm);
    $("#manage-booking-table").on("click", ".js-update-booking", loadForm);
    $("#booking-modal").on("submit", ".js-booking-update-form", saveForm);

      // Delete book
    $("#person-booking-table").on("click", ".js-delete-booking", loadForm);
    $("#manage-booking-table").on("click", ".js-delete-booking", loadForm);
    $("#booking-modal").on("submit", ".js-booking-delete-form", saveForm);
    
});

// Success modal when any changes are saved.
function Swal() {
    var span = document.createElement("span");
    span.innerHTML = "</br>" + "Your changes has been saved";
    swal({
        title: "" + "Good job!" + "",
        content: span,
        icon: "success",
        buttons: false,
        timer: 4000
    });
}


var modal = document.getElementById("booking-modal");
var modal2 = document.getElementById("modal-booking");

// Allow user to close modal by clicking on X or clicking outside modal
window.onclick = function(event) {
    if (event.target == modal || event.target == modal2 || event.target == close ) {
        $("#booking-modal").css("display", "none");
    }
};

// Tab for showing non-queued bookings
function bookedTab() {
    var list = document.getElementsByTagName("thead");
    for(var i = 0; i<list.length; i++) {
        if(list[i].getAttribute("data-no")) {
            if(list[i].getAttribute("data-no") > 0) {
                list[i].style.display = "none";
            }
            else {
                list[i].style.display = "contents";
            }
        }
    }
    var list = document.getElementsByTagName("tbody");
    for(var i = 0; i<list.length; i++) {
        if(list[i].className) {
            if(list[i].className > 0) {
                list[i].style.display = "none";
            }
            else {
                list[i].style.display = "contents";
            }
        }
    };
}

// Tab for showing queued tabs
function queuedTab() {
    var list = document.getElementsByTagName("thead");
    for(var i = 0; i<list.length; i++) {
        if(list[i].getAttribute("data-no")) {
            if(list[i].getAttribute("data-no") > 0) {
                list[i].style.display = "contents";

            }
            else {
                list[i].style.display = "none";

            }
        }
    }
    var list = document.getElementsByTagName("tbody");
    for(var i = 0; i<list.length; i++) {
        if(list[i].className) {
            if(list[i].className > 0) {
                list[i].style.display = "contents";

            }
            else {
                list[i].style.display = "none";

            }
        }
    }
}

// Script used for showing either queued or non-queued bookings.
function openTab(event, type) {
    if(type=="Queued") {
        queuedTab();
    }
    if(type=="Booked"){
        bookedTab();
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    event.currentTarget.className += " active";
}
