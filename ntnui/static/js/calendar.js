// Globally head date object for the month shown
var date = new Date();
date.setDate(1);
date.setMonth(0);

window.onload = function() {
    // Add the current month on load
    createMonth();
};

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

// Converts day ids to the relevant string
function dayOfWeekAsString(dayIndex) {
        return ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][dayIndex];
    }
    // Converts month ids to the relevant string
function monthsAsString(monthIndex) {
    return ["January", "Febuary", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][monthIndex];
}

function daySchedule(){
    //var scheduleTable = document.getElementById("scheduleTable");
    var scheduleTable = document.createElement("table");
    scheduleTable.id = "scheduleTable";
    var titlerow = scheduleTable.insertRow(0);
    var times = titlerow.insertCell(0);
    var bookings = titlerow.insertCell(1);
    times.innerHTML = "Tider";
    bookings.innerHTML = "Aktiviter";
    for(i=0;i<5;i++){
        var rows = scheduleTable.insertRow(i+1);
        var time = rows.insertCell(0);
        time.id = 8+i;
        time.innerHTML = Math.floor((8+(i/2)))+':'+((i%2/2)*60);
        var booking = rows.insertCell(1);
        booking.innerHTML = "Trening";
    }
    return scheduleTable;
}

function createBookingForm(){
    var bookingForm = document.createElement("form");
    var bookingFormTable = document.createElement("table");
    var bookingFormInput = document.createElement("input");
    bookingFormInput.type = "submit";
    bookingFormInput.value = "submit";
    bookingForm.action = "";
    bookingForm.method = "post";
    bookingForm.enctype = "multipart/form-data";
    bookingForm.innerHTML = "{% csrf_token %} {{ form.file_name }}"
    bookingFormTable.innerHTML = "name: {{form.name}}{{form.person.as_hidden}}location {{form.location}}date {{form.contact_date}}time {{form.contact_time}}"
    bookingForm.appendChild(bookingFormTable);
    bookingForm.appendChild(bookingFormInput);

    return bookingForm;
}

// Creates a day element
function createCalendarDay(num, day, mon, year, abailable) {
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
    popupSpan.className = "close";
    popupSpan.style.width = "2%"
    popupInfo.className = "dayInfo";
    popupSpan.innerHTML = "&times;"
    popupInfo.innerHTML = day + " den " + num + ". " + mon + ' ' + year +  '. Dette er en test.';
    popupContent.appendChild(popupSpan);
    popupContent.appendChild(popupInfo);
    popupTag.appendChild(popupContent);

    

    available = true;
    date.innerHTML = num;
    dayElement.innerHTML = ' ' + day;
    if(available == true){
        availability.innerHTML = "LEDIG";
        availability.style.color = "green";

    } else {
        availability.innerHTML = "FULLT";
        availability.style.color = "red";
    }

    newDay.className = "calendar-day ";

    // Set ID of element as date formatted "8-January" etc
    newDay.id = num + "-" + mon + "-" +year;
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
    //popupContent.appendChild(popupInfo);
    btn.onclick = function() {
        modal.style.display = "block";
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
    popupInfo.appendChild(daySchedule());
    popupInfo.appendChild(createBookingForm());


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
function createMonth() {
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

    getCurrentDay();
}


function getCurrentDay() {

    // Create a new date that will set as default time
    var todaysDate = new Date();
    var today = todaysDate.getDate();
    var currentMonth = todaysDate.getMonth();
    var currentYear = todaysDate.getFullYear();
    var thisMonth = monthsAsString(currentMonth);
    // Find element with the ID for today
    currentDay = document.getElementById(today + "-" + thisMonth + "-" + currentYear);
    currentDay.className = "calendar-day today";
}

$(document).on('click',jQuery(this).attr("id"),function(){
  console.log("hello")

});



