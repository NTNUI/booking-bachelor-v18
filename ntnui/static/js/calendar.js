// Globally head date object for the month shown.
var date = new Date();
var currentMonth;

// Global list to store bookings. This list will be used to populate the calendar with data.
var global_list = [];
// Ajax setting to set caching to false.
$.ajaxSetup ({
    cache: false
});

// Global variabel which is used to store the date for each popup.
var tempDay;

// Load promise object when site is loaded.
window.onload = function() {
    promise();
}

// Allows us to navigate through months with the arrow keys
document.onkeydown = function(evt) {
    evt = evt || window.event;
    switch (evt.keyCode) {
        case 37:
            previousMonth();
            break;
        case 39:
            nextMonth();
            break;
    }
}

// Promise object used to fetch data from our API.
function promiseTest() {
    return $.ajax({
        url: "/booking/api",
        dataType: "json",
        type: "GET",
        cache: false,
        success: function() {
            console.log("refresh")
        }
    })
}

// Function used to resolve promise object. When object is resolved, call createMonth and push data to global_list.
var promised = promiseTest();
var promise = function () {
promised.done(function() {
    promised.then( function() {
            createMonth();
            global_list.push(promised.responseJSON);
            currentMonth = document.getElementById("current-month");
            }
        )
    })
}
//temporary cheat
// var win = window.open('http://www.google.com');
// console.log(window.location)
// window.onbeforeunload = function(){populate()}
var getTime = function(time){
    // console.log("gettime : " +time)
    var timeArray = time.split(":");
    var hours = parseInt(timeArray[0]);
    var minutes = parseInt(timeArray[1]);
    return new Array(hours, minutes)
}
// Removes the calendar blur when filter is used
$('#search-button').click(function () {
      $('#calendar-container').css({
          'pointer-events': 'all',
          '-webkit-filter': 'blur(0px)',
          '-ms-filter': 'blur(0px)',
          'filter': 'blur(0px)',
      })
   });

// Removes the calendar blur when filter is used
$('.filter-cursors').click(function () {
        populate()
        $('#calendar-container').css({
          'pointer-events': 'all',
          '-webkit-filter': 'blur(0px)',
          '-ms-filter': 'blur(0px)',
          'filter': 'blur(0px)',
      })

   });

// Function used to populate the calendar with bookings from the database.

function populate() {

    var date_map = new Map();

    for (i = 0; i < global_list[0].length; i++) {
        var qNo = global_list[0][i].queueNo;
        var loc = global_list[0][i].location__name;
        loc = document.getElementById(loc);
        var location = global_list[0][i].location__name;
        var day = global_list[0][i].start;
        var date_format = day.slice(0, 10);
        if (qNo == 0){
            if(loc.value === location && loc.checked === true){

                var start_datetime = day.split("T");
                var start_date = start_datetime[0];
                var start_time = start_datetime[1].replace("Z", "");

                var end_datetime = global_list[0][i].end.split("T");
                var end_time = end_datetime[1].replace("Z", "");
                //find difference between end and start
                var start_array = getTime(start_time);
                var end_array = getTime(end_time);
                var diff_hour = end_array[0]-start_array[0];
                var diff_min = end_array[1]-start_array[1];
                if (date_map.has(start_date) && loc.value === location && loc.checked === true){
                    //add current hours to prior hours
                    sum_array = getTime(date_map.get(start_date));
                    var hours = diff_hour + sum_array[0];
                    var min = diff_min + sum_array[1];
                    date_map.set(start_date, ""+hours+":"+min);
                }
                else if(loc.value === location && loc.checked === true) {
                    date_map.set(start_date, ""+diff_hour+":"+diff_min)
                }

                $("#" + date_format + " h1").text(""+ (12 - parseInt(getTime(date_map.get(start_date)[0])))+" hours free");
            }
            else if (loc.checked === false){
                $("#" + date_format + " h1").text("12 hours free");
            }
        }
    }

}

//Mutation Observer
var targetNode = document.getElementById("calendar");
var config = {attributes: true, subtree: true, characterData:true};
//callback function to execute when mutations are observed
var callback = function(mutationsList){
    for (var mutation of mutationsList){
        if (mutation.type = "childList"){
            populate();
        }
        else if (mutation.type == 'attributes'){
            console.log('The ' + mutation.attributeName + ' attribute was modified');
        }
        else if ( mutation.type == 'subtree'){
            console.log("subtree")
        }
    }
}

var window = document.defaultView;
var observer = new MutationObserver(callback);
observer.observe(targetNode, config);
// Event listener. Fires whenever the calendar changes.
function HandleDOM_Change () {
    populate();
}

// Event listener logic.
// TODO: Replace with mutation observer.
fireOnDomChange ('#calendar', HandleDOM_Change, 500);


function fireOnDomChange (selector, actionFunction, delay) {

    // observer.observe(targetNode, config);

    // $(selector).on ('DOMSubtreeModified', fireOnDelay);

    // function fireOnDelay () {
    //     if (typeof this.Timer == "number") {
    //         clearTimeout (this.Timer);
    //     }
    //     this.Timer  = setTimeout (  function() { fireActionFunction (); },
    //                                 delay ? delay : 333
    //                              );
    // }

    // function fireActionFunction () {
    //     // observer.disconnect();

    //     $(selector).off ('DOMSubtreeModified', fireOnDelay);

    //     actionFunction ();
    //     $(selector).on ('DOMSubtreeModified', fireOnDelay);
    // }
}

// Converts day ids to the relevant string
function dayOfWeekAsString(dayIndex) {
    return ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][dayIndex];
}

// Converts month ids to the relevant string
function monthsAsString(monthIndex) {
    return ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"][monthIndex];
}

// Month names varibles
var monthNames = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

// Add 0 to single digit numbers.
function minTwoDigits(n) {
    return (n < 10 ? '0' : '') + n;
}

// Legacy popup.
function createPopup() {
    var popupTag = document.createElement("div");
    var popupContent = document.createElement("div");
    var popupSpan = document.createElement("span");
    popupTag.className = "modal-large";
    popupContent.className = "modal-content";
    popupContent.appendChild(popupSpan);
    popupTag.appendChild(popupContent);
    var modal = document.getElementsByClassName(popupTag.className);
    var span = document.getElementById(popupSpan.id);
    modal.style.display = "block";
    $('.modal-content').load('new',function(){}).hide().fadeIn();
}

// Creates a day element
function createCalendarDay(num, day, mon, year, available) {
    var currentCalendar = document.getElementById("calendar");
    var newDay = document.createElement("div");
    var date = document.createElement("p");
    var dayElement = document.createElement("p");
    var availability = document.createElement("h1");

    // Fills out empty days
    available = true;
    date.innerHTML = num + ".";
    dayElement.innerHTML = " " + day;
    if (available == true) {
        availability.innerHTML = "12 hours free";
        availability.style.color = "green";
    }

    //console.log(parseInt(getTime(date_map.get(start_date)[0])));

    //if(12 - parseInt(getTime(date_map.get(start_date)[0])) > 6){
    //    availability.style.color = "green";
    //}else if(12 - parseInt(getTime(date_map.get(start_date)[0])) > 2){
    //    availability.style.color = "yellow";
    //}else{
    //    availability.style.color = "red";
    //}

    newDay.className = "calendar-day";
    newDay.title = "Click to book";
    // Set ID of element as date formatted "8-January" etc
    num = minTwoDigits(num);
    newDay.id = year + "-" + mon + "-" + num;
    currentCalendar.style.width = "100%;"
    newDay.appendChild(date)
    newDay.appendChild(dayElement);
    newDay.appendChild(availability);
    currentCalendar.appendChild(newDay);
    var btn = document.getElementById(newDay.id);
    // call popup function and pass event.target.
    btn.onclick = function (e) {
        popup(this, e);
    }

    // Restricts days that cant be booked
    if (newDay.id < getCurrentDay()) {
        newDay.className = "calendar-day restricted";
    }
    return newDay
}


// Clears all days from the calendar
    function clearCalendar() {
        var currentCalendar = document.getElementById("calendar");
        currentCalendar.innerHTML = "";

    }

// Clears the calendar and shows the next month
    function nextMonth() {
        clearCalendar();
        date.setMonth(date.getMonth() + 1);
        createMonth(date.getMonth());
    }

// Clears the calendar and shows the previous month
    function previousMonth() {
        clearCalendar();
        date.setMonth(date.getMonth() - 1);
        var val = date.getMonth();
        createMonth(date.getMonth());
        return val
    }

    function daysInMonth(month, year) {
        return new Date(year, month, 0).getDate();
    }

// Creates and populates all of the days to make up the month
    function createMonth() {
        date.setDate(1);
        var dateObject = new Date();
        dateObject.setDate(date.getDate());
        dateObject.setMonth(date.getMonth());
        dateObject.setYear(date.getFullYear());
        var days;
        var count = 0;
        var length = daysInMonth(date.getMonth() + 1, date.getFullYear())
        for (days = 0; days < length; days++) {
            while (count < 6) {
                count += 0;
                if (date.getDay() == 0) {
                    createCalendarDay("dummy", dateObject.getDate(),
                        dayOfWeekAsString(dateObject.getDay()),
                        monthsAsString(dateObject.getMonth()),
                        dateObject.getFullYear()).style.visibility = "hidden";
                }
                if (date.getDay() == 2) {
                    count += 5;
                    createCalendarDay("dummy", dateObject.getDate(),
                        dayOfWeekAsString(dateObject.getDay()),
                        monthsAsString(dateObject.getMonth()),
                        dateObject.getFullYear()).style.visibility = "hidden"
                }
                if (date.getDay() == 3) {
                    count += 4;
                    createCalendarDay("dummy", dateObject.getDate(),
                        dayOfWeekAsString(dateObject.getDay()),
                        monthsAsString(dateObject.getMonth()),
                        dateObject.getFullYear()).style.visibility = "hidden"
                }
                if (date.getDay() == 4) {
                    count += 1.2;
                    createCalendarDay("dummy", dateObject.getDate(),
                        dayOfWeekAsString(dateObject.getDay()),
                        monthsAsString(dateObject.getMonth()),
                        dateObject.getFullYear()).style.visibility = "hidden"
                }
                if (date.getDay() == 5) {
                    count += 0.5;
                    createCalendarDay("dummy", dateObject.getDate(),
                        dayOfWeekAsString(dateObject.getDay()),
                        monthsAsString(dateObject.getMonth()),
                        dateObject.getFullYear()).style.visibility = "hidden"
                }
                if (date.getDay() == 6) {
                    count += 0.2
                    createCalendarDay("dummy", dateObject.getDate(),
                        dayOfWeekAsString(dateObject.getDay()),
                        monthsAsString(dateObject.getMonth()),
                        dateObject.getFullYear()).style.visibility = "hidden"
                }
                count += 1
            }
            createCalendarDay(dateObject.getDate(),
                dayOfWeekAsString(dateObject.getDay()),
                monthsAsString(dateObject.getMonth()),
                dateObject.getFullYear());

            dateObject.setDate(dateObject.getDate() + 1);
            count += 1;
        }

        // Set the text to the correct month
        var currentMonthText = document.getElementById("current-month");
        currentMonthText.innerHTML = monthNames[date.getMonth()] + " " + date.getFullYear();

        // Gives the current date a highligth
        var current_day = getCurrentDay();
        document.getElementById(current_day).className = "calendar-day today";
    }

//Get the current day
    function getCurrentDay() {
        var todaysDate = new Date();
        var today = todaysDate.getDate();
        // add 0 to single digit days
        var today_formatted = minTwoDigits(today);
        var currentMonth = todaysDate.getMonth();
        var currentYear = todaysDate.getFullYear();
        var currentMonthString = monthsAsString(currentMonth);
        var current_day = (currentYear + "-" + currentMonthString + "-" + today_formatted).toString();
        return current_day
    }

//Opens the modal with content */
    function popup(e) {

        $.ajax({
            url: '/booking/bookings_list/create_calendar/',
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $("#booking-modal .booking-modal-contents").html("");
                $('#booking-modal').fadeTo(100, function () {
                    $(this).css("display", "inline-block");
                }).fadeTo(300, 1);
            },
            success: function (data) {
                $("#booking-modal .booking-modal-contents").html(data.html_form);

            }

        });

        //Set global tempDay variable to event that triggers the popup, ie the date.
        this.tempDay = e;

        var modal = document.getElementById('booking-modal');
        // Get the <span> element that closes the modal
        var span = document.getElementsByClassName("close")[0];
        modal.style.display = "block";
        // When the user clicks anywhere outside of the modal, close it

        window.onclick = function (event) {

            if (event.target == modal) {
                modal.style.display = "none";


            }
            else if (event.target == close) {
                console.log("closed!")
                modal.style.display = "none"
                //location.reload();

            }
        }
    }

// Dropdown for filtering
    function dropdownFilters(event){
        var toggleArrow = document.getElementById(event.target.id);
        toggleArrow.classList.toggle("down");
        var typeId = toggleArrow.nextSibling.nextSibling.id;
        var toggleType = document.getElementById(typeId);
        toggleType.style.display = toggleType.style.display == "block" ? "none" : "block";
    };
/*
    document.getElementById("dropdown").onclick = function(){
        var toggle = document.getElementById('filter-type');
        toggle.style.display = toggle.style.display == "block" ? "none" : "block";
        var toggleArrow = document.getElementById("dropdown");
        toggleArrow.classList.toggle("down");
    };*/


