function ajaxForm() {
    var myForm = $('#createform');
    event.preventDefault()
    var start_time = document.getElementById("startInput").value;
    var end_time = document.getElementById("endInput").value;
    var $form_data = $(myForm).serialize()+"&start="+tempDay.id.toString() + " " + start_time + "&end="+tempDay.id.toString() + " " + end_time + "&location=" + " " + chosenLocation;
    $.ajax({
        method: "POST",
        url: '/booking/bookings_list/create_calendar/',
        data: $form_data,
        complete: function(data) {
            var modal = document.getElementById('booking-modal');
            modal.style.display = "none";
            var promised = promiseTest();
            promised.done(function() {
                promised.then( function() {
                    global_list = []
                    console.log("promised")
                    global_list.push(promised.responseJSON);
                })
            })
        },
    })
}

var list_of_bookings = []
var chosenLocation = this.currentLocation;
var booking_data; //global variable for booking data
var overlap = []; //put overlapping bookings here
$(document).ready(function(){

    document.getElementById("id_day").value=tempDay.children[1].innerHTML.trim();
    var btn = document.getElementById("submission");
    $(btn).click(function () {
        if(validateForm()) {
            var count = 0;
            $( list_of_bookings ).each(function( index ) {
                if (list_of_bookings[index][5] == 0) {
                    var start_time = document.getElementById("startInput").value;
                    var end_time = document.getElementById("endInput").value;
                    var s = list_of_bookings[index][1].replace(":", "");
                    var e = list_of_bookings[index][2].slice(11, 16).replace(":", "");
                    var s0 = start_time.slice(0, 5).replace(":", "");
                    var e0 = end_time.slice(0, 5).replace(":", "");
                    if ((s <= s0 && e > s0) || (s > s0 && s < e0) || (s < s0 && e > e0)) {
                        count += 1;
                    }
                }
            });
            if (count != 0) {
                swal({
                    title: "Ops! Looks like a booking already exists on that time range",
                    text: "Do you want to enqueue your booking?",
                    buttons: ["No", "Yes"],
                    successMode: true,
                }).then((willQueue) => {
                    if (willQueue) {
                        var recurringRequest = document.getElementById("id_repeat");
                        if (recurringRequest.value != "noRepeat") {
                            console.log("recurring")
                            swal({
                                title: "Do you want to request a recurring booking?",
                                text: "This request will be reviewed by NTNUi staff",
                                buttons: ["No", "Yes"],
                                successMode: true,
                            }).then((Request) => {
                                if(Request) {
                                    var span = document.createElement("span");
                                    span.innerHTML = "You can find your queued booking at " + '</br>' + " <a href=\"/booking/bookings_list\">My Bookings</a>";
                                    swal({
                                        title: "" + "Great, you have queued a booking!" + "",
                                        content: span,
                                        icon: "success",
                                        buttons: false,
                                        timer: 4000,
                                    });
                                    ajaxForm()
                                }
                            })
                        }
                        else {
                            var span = document.createElement("span");
                            span.innerHTML = "You can find your queued booking at " + '</br>' + " <a href=\"/booking/bookings_list\">My Bookings</a>";
                            swal({
                                title: "" + "Great, you have queued a booking!" + "",
                                content: span,
                                icon: "success",
                                buttons: false,
                                timer: 4000,
                            });
                            ajaxForm()
                        }
                    }
                });
            } else {
                var recurringRequest = document.getElementById("id_repeat");
                if (recurringRequest.value != "noRepeat") {
                            swal({
                                title: "Do you want to request a recurring booking?",
                                text: "This request will be reviewed by NTNUi staff?",
                                buttons: ["No", "Yes"],
                                successMode: true,
                            }).then((Request) => {
                                if(Request) {
                                    var span = document.createElement("span");
                                    span.innerHTML = "You can find your booking at " + '</br>' + " <a href=\"/booking/bookings_list\">My Bookings</a>";
                                    swal({
                                        title: "" + "Great, you have made a booking!" + "",
                                        content: span,
                                        icon: "success",
                                        buttons: false,
                                        timer: 4000,
                                    });
                                    ajaxForm()
                                }
                            })
                        }
                else {
                    var span = document.createElement("span");
                    span.innerHTML = "You can find your booking at " + '</br>' + " <a href=\"/booking/bookings_list\">My Bookings</a>";
                    swal({
                        title: "" + "Great, you have made a booking!" + "",
                        content: span,
                        icon: "success",
                        buttons: false,
                        timer: 4000,
                    });
                    ajaxForm()
                }
            }
        }
    });
});