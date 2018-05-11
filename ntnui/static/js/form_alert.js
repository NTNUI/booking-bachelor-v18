// Checks if overlapping and triggers sweet alert or creating the booking
var bookings = [];
var chosenLocation = this.currentLocation;
var booking_data; // Global variable for booking data
$(document).ready(function(){
    if ($('#id_day').length){
        document.getElementById("id_day").value = new Date(tempDay.id.substring(0, 4), +
                tempDay.id.substring(5,7) - 1, tempDay.id.substring(8, 10)).toString().slice(0, 3);
    }
    var btn = document.getElementById("submission");
    $(btn).click(function(){
        if(validateForm()){
            var count = 0;
            $( bookings ).each(function( index ) {
                if (bookings[index][5] == 0) {
                    var start_time = document.getElementById("startInput").value;
                    var end_time = document.getElementById("endInput").value;
                    var s = bookings[index][1].replace(":", "");
                    var e = bookings[index][2].slice(11, 16).replace(":", "");
                    var s0 = start_time.slice(0, 5).replace(":", "");
                    var e0 = end_time.slice(0, 5).replace(":", "");
                    // Checking if times are overlapping with other bookings on that day
                    if ((s <= s0 && e > s0) || (s > s0 && s < e0) || (s < s0 && e > e0)) {
                        count += 1;
                    }
                }
            });
            if(count != 0){
                swal({
                    title: "Ops! Looks like a booking already exists on that time range",
                    text: "Do you want to enqueue your booking?",
                    buttons: ["No", "Yes"],
                    successMode: true,
                }).then((willQueue) => {
                    if(willQueue){
                        var span = document.createElement("span");
                        span.innerHTML = "You can find your queued booking at " + '</br>' +
                            "<a href=\"/booking/bookings_list\">My Bookings</a>";
                        swal({
                            title: "" + "Great, you have queued a booking!" + "",
                            content: span,
                            icon: "success",
                            buttons: false,
                            timer: 4000
                        });
                        var myForm = $('#createform');
                        event.preventDefault();
                        // append start date to post request
                        var start_time = document.getElementById("startInput").value;
                        var end_time = document.getElementById("endInput").value;
                        var $form_data = $(myForm).serialize() + "&start=" + tempDay.id.toString() +
                            " " + start_time + "&end=" + tempDay.id.toString() + " " +
                            end_time + "&location=" + " " + chosenLocation;
                        $.ajax({
                            method: "POST",
                            url: '/booking/bookings_list/create_calendar/',
                            data: $form_data,
                            complete: function(data) {
                                var modal = document.getElementById('booking-modal');
                                modal.style.display = "none";
                                var promised = promiseTest();
                                promised.done(function(){
                                    promised.then( function(){
                                        globalList = [];
                                        globalList.push(promised.responseJSON);
                                    })
                                })
                            }
                        })
                    }
                });
            } else {
                var span = document.createElement("span");
                span.innerHTML = "You can find your booking at " + '</br>' +
                    "<a href=\"/booking/bookings_list\">My Bookings</a>";
                swal({
                    title: "" + "Great, you have made a booking!" + "",
                    content: span,
                    icon: "success",
                    buttons: false,
                    timer: 4000
                });
                var myForm = $('#createform');
                event.preventDefault();
                // append start date to post request
                var start_time = document.getElementById("startInput").value;
                var end_time = document.getElementById("endInput").value;
                var $form_data = $(myForm).serialize() + "&start=" + tempDay.id.toString() +
                    " " + start_time + "&end=" + tempDay.id.toString() + " " + end_time +
                    "&location=" + " " + chosenLocation;
                $.ajax({
                    method: "POST",
                    url: '/booking/bookings_list/create_calendar/',
                    data: $form_data,
                    complete: function(data){
                        var modal = document.getElementById('booking-modal');
                        modal.style.display = "none";
                        var promised = promiseTest();
                        promised.done(function(){
                            promised.then( function() {
                                globalList = [];
                                globalList.push(promised.responseJSON);
                                populate();
                            })
                        })
                    }
                })
            }
        }
    });
});