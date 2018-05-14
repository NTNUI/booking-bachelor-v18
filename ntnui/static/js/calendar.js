// Globally head date object for the month shown.
var date = new Date();

// Variable used for setting calendar month name
var currentMonth;

// Global variable for storing current calendar month
var currentCalendarMonth;

// Global list to store bookings. This list will be used to populate the calendar with data.
var globalList = [];

// Global variabel which is used to store the date for each popup.
var tempDay;

// Globla variable for storing current location ID and string name
var currentLocation;
var locationString;

// Ajax setting to set caching to false.
$.ajaxSetup ({
    cache: false
});

// Load promise object when site is loaded and triggers filter alert
window.onload = function() {
    promise();
    triggerFilterAlert();
};

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
};

// Promise object used to fetch data from our API.
function promiseTest() {
    return $.ajax({
        url: "/booking/api",
        dataType: "json",
        type: "GET",
        cache: false,
    })
}

// Function used to resolve promise object. When object is resolved, call createMonth and push data to globalList.
var promised = promiseTest();
var promise = function () {
    promised.done(function() {
        promised.then( function() {
            createMonth();
            globalList.push(promised.responseJSON);
            currentMonth = document.getElementById("current-month");
            }
        )
    })
};

// Convert "HH:MM" to [H, M]
var getTime = function(time){
    var timeArray = time.split(":");
    var hours = parseInt(timeArray[0]);
    var minutes = parseInt(timeArray[1]);
    return new Array(hours, minutes)
};

// Function used to populate the calendar with bookings from the database and show available hours.
function populate() {
    var dateMap = new Map(); // Store sum of hours and minutes for a date
    for (var i = 0; i < globalList[0].length; i++) {
        var qNo = globalList[0][i].queueNo;
        var locationId = globalList[0][i].location__name;
        var location = document.getElementById(locationId);
        var day = globalList[0][i].start;
        var dateFormat = day.slice(0, 10);
        var startDatetime = day.split("T");
        var startDate = startDatetime[0];
        if (qNo == 0){
            if(location.checked === true){
                var startTime = startDatetime[1].replace("Z", "");
                var endDatetime = globalList[0][i].end.split("T");
                var endTime = endDatetime[1].replace("Z", "");
                // Find difference between end and start
                var startArray = getTime(startTime);
                var endArray = getTime(endTime);
                var diffHour = endArray[0]-startArray[0];
                var diffMin = endArray[1]-startArray[1];
                if (dateMap.has(startDate) && location.value === locationId && location.checked === true){
                    // Add current hours to prior hours
                    var sumArray = getTime(dateMap.get(startDate));
                    var hours = diffHour + sumArray[0];
                    var min = diffMin + sumArray[1];
                    dateMap.set(startDate, "" + hours + ":" + min);
                }else if(location.value === locationId && location.checked === true) {
                    dateMap.set(startDate, "" + diffHour + ":" + diffMin);
                }
                // Change the html in the calendar boxes with number of booked hours.
                if(12-parseInt(getTime(dateMap.get(startDate))[0]) >= 0){
                    $("#" + dateFormat + " h1").text(
                        "" + (12 - parseInt(getTime(dateMap.get(startDate))[0]))
                        + "\n" + " hours free")
                }
                if(12-parseInt(getTime(dateMap.get(startDate))[0]) > 9) {
                    $("#" + dateFormat + " h1").css("color", "#fc8307");
                }else if(12-parseInt(getTime(dateMap.get(startDate))[0]) > 5){
                    $("#" + dateFormat + " h1").css("color", "#fc5908");
                }else if(12-parseInt(getTime(dateMap.get(startDate))[0]) >= 1){
                    $("#" + dateFormat + " h1").css("color", "#f73717");
                }else if(12-parseInt(getTime(dateMap.get(startDate))[0]) < 1){
                    $("#" + dateFormat + " h1").css("color", "red");
                }
            }else if(dateMap.has(startDate) === false) {
                $("#" + dateFormat + " h1").text("12" + "\n" + "hours free").css("color", "green");
            }
        }
    }
}

//Mutation Observer
var targetNode = document.getElementById("calendar");

var config = {attributes: false, subtree: true, characterData:true};

// Callback function to execute when mutations are observed
var callback = function(mutationsList){};

var window = document.defaultView;
var observer = new MutationObserver(callback);
observer.observe(targetNode, config);

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
    return (n < 10 ? "0" : "") + n;
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
    newDay.className = "calendar-day";
    newDay.title = "Click to book";

    // Set ID of element as date formatted "8-January" etc
    num = minTwoDigits(num);
    newDay.id = year + "-" + mon + "-" + num;
    currentCalendar.style.width = "100%;";
    newDay.appendChild(date);
    newDay.appendChild(dayElement);
    newDay.appendChild(availability);
    currentCalendar.appendChild(newDay);
    var dayBtn = document.getElementById(newDay.id);

    // call popup function and pass event.target and modalTitle to fill inn title.
    dayBtn.onclick = function (e) {
        popup(this, e);
    };

    var maxMonth;
    var maxDay;
    var currentDate = new Date;
    // Restricts days that cant be booked. Stops at 10. june in spring and 21. desember in autumn
    if(currentDate.getMonth()+1 <= 6){
        maxMonth = "0" + 6;
    }
    if(currentDate.getMonth()+1 >= 8){
        maxMonth = 12;
        maxDay = 20;
    }
    if (newDay.id < getCurrentDay() || newDay.id > currentDate.getFullYear()+"-"+maxMonth+"-"+maxDay) {
        newDay.className = "calendar-day restricted";
    }
    return newDay;
}


// Clears all days from the calendar
function clearCalendar() {
    var currentCalendar = document.getElementById("calendar");
    currentCalendar.innerHTML = "";

}

// Clears the calendar and shows the next month
function nextMonth() {
    clearCalendar();
    date.setMonth(this.currentCalendarMonth.getMonth() + 1);
    createMonth(this.currentCalendarMonth.getMonth());
    populate();
}

// Clears the calendar and shows the previous month
function previousMonth() {
    clearCalendar();
    date.setMonth(this.currentCalendarMonth.getMonth() - 1);
    var val = date.getMonth();
    createMonth(this.currentCalendarMonth.getMonth());
    populate();
    return val;
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
    var length = daysInMonth(date.getMonth() + 1, date.getFullYear());
    for (days = 0; days < length; days++) {
        while (count < 6) {
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
                dateObject.getFullYear()).style.visibility = "hidden";
            }
            if (date.getDay() == 3) {
                count += 4;
                createCalendarDay("dummy", dateObject.getDate(),
                dayOfWeekAsString(dateObject.getDay()),
                monthsAsString(dateObject.getMonth()),
                dateObject.getFullYear()).style.visibility = "hidden";
            }
            if (date.getDay() == 4) {
                count += 1.2;
                createCalendarDay("dummy", dateObject.getDate(),
                dayOfWeekAsString(dateObject.getDay()),
                monthsAsString(dateObject.getMonth()),
                dateObject.getFullYear()).style.visibility = "hidden";
            }
            if (date.getDay() == 5) {
                count += 0.5;
                createCalendarDay("dummy", dateObject.getDate(),
                dayOfWeekAsString(dateObject.getDay()),
                monthsAsString(dateObject.getMonth()),
                dateObject.getFullYear()).style.visibility = "hidden";
            }
            if (date.getDay() == 6) {
                count += 0.2;
                createCalendarDay("dummy", dateObject.getDate(),
                dayOfWeekAsString(dateObject.getDay()),
                monthsAsString(dateObject.getMonth()),
                dateObject.getFullYear()).style.visibility = "hidden";
            }
            count += 1;
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

    // Gives the current date a highlight
    var todaysDate = new Date();
    if(dateObject.getMonth() == todaysDate.getMonth()+1 && dateObject.getYear() == todaysDate.getYear()){
        var currentDay = getCurrentDay();
        document.getElementById(currentDay).className = "calendar-day today";
    }
    this.currentCalendarMonth = date;
}

// Get the current day
function getCurrentDay() {
    var todaysDate = new Date();
    var today = todaysDate.getDate();
    // add 0 to single digit days
    var todayFormatted = minTwoDigits(today);
    var currentMonth = todaysDate.getMonth();
    var currentYear = todaysDate.getFullYear();
    var currentMonthString = monthsAsString(currentMonth);
    var currentDay = (currentYear + "-" + currentMonthString + "-" + todayFormatted);
    return currentDay;
}

// Opens the modal with content
function popup(e) {
    $.ajax({
        url: "/booking/bookings_list/create_calendar/",
        type: "get",
        dataType: "json",
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
    // Set global tempDay variable to event that triggers the popup, ie the date.
    this.tempDay = e;
    var modal = document.getElementById('booking-modal');
    modal.style.display = "block";
}

// populate calendar and get location of filter type.
function getLocation(event){
    populate();
    var locationId = event.target.getAttribute("data-id");
    var locationName = event.target.innerHTML;
    var locationTitle = event.target.title;
    var locationAdr = document.getElementById("adr").innerText;
    this.currentLocation = locationId;
    this.locationString = locationName;
    // Creating tooltip element
    var tooltip = document.createElement("div");
    tooltip.innerHTML = "&#9432;";
    tooltip.className = "tooltip-info";
    var tooltipText = document.createElement("span");
    tooltip.appendChild(tooltipText);
    tooltipText.className = "tooltip-text";
    tooltipText.innerHTML = locationTitle + "<br>" + "ADDR: " + locationAdr;
    // Adding locationName and tooltip to calendar header
    document.getElementById("current-location").innerHTML = locationName;
    document.getElementById("current-location").appendChild(tooltip);
}






