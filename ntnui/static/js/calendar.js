// Globally head date object for the month shown
var date = new Date();
date.setDate(1);
date.setMonth(0);
var global_list = [];

window.onload = function() {
    // Add the current month on load
    promise();
};

/* document.onkeydown = function(evt) {
    evt = evt || window.event;
    switch (evt.keyCode) {
        case 37:
            previousMonth();
            break;
        case 39:
            nextMonth();
            break;
    }
}; */

function promiseTest() {
    return $.ajax({
        url: "/booking/api",
        dataType: "json",
        type: "GET"
    })
}

var promised = promiseTest();

function promise() {
promised.done(function() {

    promised.then( function() {
            createMonth();
            let list = [];
            list.push(promised.responseJSON);
            global_list.push(promised.responseJSON)
            init(list);
        }
    )
});
}

function init(list) {
    for (i = 0; i < list[0].length; i++) {
        var day = list[0][i].start;
        var date_format = day.slice(0, 10);
        $("#" + date_format + " h1").text("BUSY");
        if($("#" + date_format).length == 0) {
  $("#" + date_format + " h1").text("BUSY");
}
    }

}

function HandleDOM_Change (list) {
    console.log(global_list)
    for (i = 0; i < global_list[0].length; i++) {
        var day = global_list[0][i].start;
        var date_format = day.slice(0, 10);
        $("#" + date_format + " h1").text("BUSY");
    }
    }

//--- Narrow the container down AMAP.
fireOnDomChange ('#calendar', HandleDOM_Change, 500);


function fireOnDomChange (selector, actionFunction, delay)
{
    $(selector).bind ('DOMSubtreeModified', fireOnDelay);

    function fireOnDelay () {
        if (typeof this.Timer == "number") {
            clearTimeout (this.Timer);
        }
        this.Timer  = setTimeout (  function() { fireActionFunction (); },
                                    delay ? delay : 333
                                 );
    }

    function fireActionFunction () {
        $(selector).unbind ('DOMSubtreeModified', fireOnDelay);
        actionFunction ();
        $(selector).bind ('DOMSubtreeModified', fireOnDelay);
    }
}

/*
// Gets bookings from the booking API. Will run once the page DOM is ready (the calendar is loaded)
    $(document).ready(function () {
    $.ajax({
        type: "GET",
        url: "/booking/api",
        cache: false,
        success: function (text) {
            console.log("ajax success")
            // pass down variable temp to the next jQuery function
            var temp = text;
            // Executes when the 'success' event is triggered.
            $(window).bind('load', function(text) {
                    // pass down variable to the next jQuery function
                    var temp2 = temp;
                    this.list = temp2;
                    // iterate through calendar-day div classes
                   /* $('.calendar-day ').each(function(i, obj, text) {
                        var temp3 = temp2;
                        // iterate through bookings
                        for(i=0;i<temp3.length;i++){
                           // change booking date format to yyyy-mm-dd
                           var date_format = temp3[i].start.slice(0, 10);
                           // check to see if booking start date matches the calendar-day id.
                           if(obj.id == date_format) {
                                // change h1 in matches
                                $("#"+obj.id+" h1").text("Delvis opptatt");
                           }
                        }
                    });
                });
        }

    });
}); */



// Converts day ids to the relevant string
function dayOfWeekAsString(dayIndex) {
        return ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][dayIndex];
    }
    // Converts month ids to the relevant string
function monthsAsString(monthIndex) {
    return ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"][monthIndex];
}


/* function daySchedule(bookingTime, bookingLengths){
    //var scheduleTable = document.getElementById("scheduleTable");
    bookingTime = 15;
    bookingLengths = 5;
    var scheduleTable = document.createElement("table");
    scheduleTable.className = "table borderless";
    scheduleTable.id = "scheduleTable";
    var titlerow = scheduleTable.insertRow(0);
    var times = titlerow.insertCell(0);
    titlerow.style.fontWeight =  'bold';
    var bookings = titlerow.insertCell(1);
    times.innerHTML = "Tider";
    bookings.innerHTML = "Aktiviter";
    var bookingStart = "kødder";
    var bookingEnd = "slapper av";
    for(i=0;i<31;i++){
        var rows = scheduleTable.insertRow(i+1);
        var time = rows.insertCell(0);
        rows.id = 8+i/2;
        var extravariable = ''
        if(Math.floor((8+(i/2)))<10){extravariable= '0'};
        time.innerHTML = extravariable + Math.floor((8+(i/2)))+':'+(((i%2/2)*60) + '0')[0] + (((i%2/2)*60) + '0')[1];
        var booking = rows.insertCell(1);
        booking.innerHTML = ' ';
        booking.id = "booking"+(8+i/2);
        console.log(+bookingLengths+ +bookingTime);
        if(rows.id == bookingTime){
            booking.innerHTML = bookingStart;

        } if(rows.id == bookingTime+(bookingLengths-0.5)){
            booking.innerHTML = bookingEnd;
        }if(rows.id>=bookingTime && rows.id<=bookingTime+(bookingLengths-0.5)){
            booking.style.backgroundColor = "green";
        }
    }

    return scheduleTable;
} */

function minTwoDigits(n) {
  return (n < 10 ? '0' : '') + n;
}


// Creates a day element
function createCalendarDay(num, day, mon, year, available) {
    var currentCalendar = document.getElementById("calendar");

    var newDay = document.createElement("div");
    var date = document.createElement("p");
    var dayElement = document.createElement("p");
    var availability = document.createElement("h1");
    //popup elements
    var popupTag = document.createElement("div");
    var popupContent = document.createElement("div");
    var popupSpan = document.createElement("span");
    var popupInfo = document.createElement("h1")
    popupTag.className = "modal-large";
    popupContent.className = "modal-content";
    popupContent.appendChild(popupSpan);
    popupContent.appendChild(popupInfo);
    popupTag.appendChild(popupContent);



    available = true;
    date.innerHTML = num;
    dayElement.innerHTML = ' ' + day;
    if(available == true){
        availability.innerHTML = "-";
        availability.style.color = "green";

    } else {
        availability.innerHTML = "FULLT";
        availability.style.color = "red";
    }

    newDay.className = "calendar-day ";

    // Set ID of element as date formatted "8-January" etc
    num = minTwoDigits(num);
    newDay.id = year + "-" + mon + "-" + num;
    popupTag.id = "popup"+newDay.id;
    currentCalendar.style.width = "100%;"
    popupSpan.id = "span"+newDay.id;
    newDay.appendChild(date)
    newDay.appendChild(dayElement);
    newDay.appendChild(availability);
    currentCalendar.appendChild(newDay);
    document.body.appendChild(popupTag);

    // popup

    var modal = document.getElementById(popupTag.id);
    var btn = document.getElementById(newDay.id);
    var span = document.getElementById(popupSpan.id);
    //popupContent.appendChild($(".modal-content").load("new"););
    btn.onclick = function() {
        modal.style.display = "block";
        //$(".modal-content").load("new");
        $('.modal-content').load('new',function(){}).hide().fadeIn();
        console.log("open");
    }
    span.onclick = function() {
        modal.style.display = "none";
        console.log("close");
    }
    popupTag.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
    }
    }
    // apply info to popup
    // popupInfo.appendChild(daySchedule());
    //popupInfo.appendChild(createBookingForm());
    return availability;
};


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
}

// Creates and populates all of the days to make up the month
function createMonth(updateMonth) {
    var currentCalendar = document.getElementById("calendar");

    var dateObject = new Date();
    dateObject.setDate(date.getDate());
    dateObject.setMonth(date.getMonth());
    dateObject.setYear(date.getFullYear());

    createCalendarDay(dateObject.getDate(), dayOfWeekAsString(dateObject.getDay()), monthsAsString(dateObject.getMonth()), dateObject.getFullYear());

    dateObject.setDate(dateObject.getDate() + 1);

    while (dateObject.getDate() != 1) {
        createCalendarDay(dateObject.getDate(), dayOfWeekAsString(dateObject.getDay()), monthsAsString(dateObject.getMonth()), dateObject.getFullYear());
        dateObject.setDate(dateObject.getDate() + 1);
    }

    // Set the text to the correct month
    var currentMonthText = document.getElementById("current-month");
    currentMonthText.innerHTML = monthsAsString(date.getMonth()) + " " + date.getFullYear();

    //getCurrentDay();


}


function getCurrentDay() {

    var todaysDate = new Date();
    var today = todaysDate.getDate();
    // add 0 to single digit days
    var today_formatted = minTwoDigits(today);
    var currentMonth = todaysDate.getMonth();
    var currentYear = todaysDate.getFullYear();
    var thisMonth = monthsAsString(currentMonth);
    var current_day = (currentYear + "-" + thisMonth + "-" + today_formatted).toString();
    var get_currentDay = document.getElementById(current_day);
    console.log(get_currentDay)
    document.getElementById(current_day).className = "calendar-day today";
}

// Create activity for table


