// Resets both timers if the user wants to change starttime
function resetClock(){
    var clockTicks = document.getElementsByClassName('clockpicker-tick');
    var endTime = document.getElementById('endInput');
    for(var i=0;i<clockTicks.length; i++){
        if(clockTicks.length == 28)
            if(clockTicks[i].innerHTML >= 10 && clockTicks[i].innerHTML < 23 ||
                    (clockTicks[i].innerHTML == '00' && i >(+ clockTicks.length - 4))){
                clockTicks[i].style.color = "black";
                clockTicks[i].style.pointerEvents = "auto";
                endTime.value = 'Choose end time';
                endTime.disabled = true;
            }
        if(clockTicks.length == 56){
            if(clockTicks[i].innerHTML >= 10 && clockTicks[i].innerHTML < 23 ||
                    (clockTicks[i].innerHTML == '00' && i >(+ clockTicks.length - 36))){
                clockTicks[i].style.color = "black";
                clockTicks[i].style.pointerEvents = "auto";
                endTime.value = 'Choose end time';
                endTime.disabled = true;
            }
        }
    }
}

// Edits the clockpicker so that invalid times cant be picked.
function editClock(){
    var clockTicks = document.getElementsByClassName('clockpicker-tick');
    var startTime = document.getElementById('startInput');
    var startHour = startTime.value.substring(0,2);
    for(var i=0;i<clockTicks.length; i++){
        if((clockTicks[i].innerHTML < + startHour + 1 ||
                clockTicks[i].innerHTML < 10) && i < ( + clockTicks.length - 4)){
            clockTicks[i].style.color = "#DCDCDC";
            clockTicks[i].style.pointerEvents = "none";
        }
    }
}

// Checks if starttime is picked before endtime is able to be picked
function checkStartTime(){
    var startTime = document.getElementById('startInput');
    var endTime = document.getElementById('endInput');
    var endTimeSpan = document.getElementById('endTimeSpan');
    if(startTime){
        if(startTime.value == 'Choose start time'){
            endTime.disabled = true;
            endTimeSpan.style.pointerEvents = "none";
        }
    }
    if(startTime.value != 'Choose start time'){
        endTime.disabled = false;
        endTimeSpan.style.pointerEvents = "auto";
    }
}

// Edits minimum date and maximum date of the timepicker. Stops at the end of the semester
function minMaxDate(){
    var today = new Date();
    var dd = today.getDate();
    var mm = today.getMonth() + 1;
    var yyyy = today.getFullYear();
        if(dd < 10){
            dd = '0' + dd;
        }
        if(mm < 10){
            mm = '0' + mm;
        }
    today = yyyy + '-' + mm + '-' + dd;
    var maxdd;
    var maxmm;
    if(mm <= 6){
        maxmm = '0' + 6;
        maxdd = 10;
    }
    if(mm >= 8){
        maxmm = 12;
        maxdd = 21;
    }
    var maxDate = yyyy + '-' + maxmm + '-' + maxdd;
    document.getElementById('date').setAttribute('min', today);
    document.getElementById('date').setAttribute('max', maxDate);
}

// Gets date and week for calendar form
var formattedDate = new Date(tempDay.id.substring(0,4), + tempDay.id.substring(5,7)-1, tempDay.id.substring(8,10));
document.getElementById('dayTitle').innerHTML = dayOfWeekAsString(formattedDate.getDay()) + ' '
    + formattedDate.getDate() + '. ' + monthNames[formattedDate.getMonth()] + '<h5>' + locationString + '</h5>';

var weekly = document.getElementById("id_repeat").children[1];
weekly.innerHTML = 'Repeat every '+dayOfWeekAsString(formattedDate.getDay());

// Closes modal when clicking outside or on close
window.onclick = function(event) {
    if (event.target == modal || event.target == modal2 || event.target == close ) {
        $("#booking-modal").css("display", "none");
    }
};
