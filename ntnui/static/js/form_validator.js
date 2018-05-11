// Validation for the form
function validateForm() {
    var description = document.forms["createform"]["id_description"];
    var title = document.forms["createform"]["id_title"];
    var start = document.forms["createform"]["startInput"];
    var end = document.forms["createform"]["endInput"];
    var error = "";
    var errorMessage = document.getElementById("errorMessage");
    errorMessage.innerHTML = "";
    if(title.value === "") {
        title.style.border = "1px solid red";
        error += "title ";
        errorMessage.innerHTML += "Title cannot be empty.";
        $(title).click(function () {
            title.style.border = "1px solid rgba(0,0,0,.15)"
        })
    }if(description.value === "") {
        description.style.border = "1px solid red";
        error += "description ";
        errorMessage.innerHTML += "<br> Description cannot be empty.";
        $(description).click(function () {
            description.style.border = "1px solid rgba(0,0,0,.15)"
        })
    }
    if(start.value === "Choose start time") {
        start.style.border = "1px solid red";
        error += "start ";
        errorMessage.innerHTML += "<br> Must choose start time.";
        $(start).click(function () {
            start.style.border = "1px solid rgba(0,0,0,.15)"
        });
    }
    if(end.value === "Choose end time") {
        end.style.border = "1px solid red";
        error += "end ";
        errorMessage.innerHTML += "<br> Must choose end time.";
        $(end).click(function () {
            end.style.border = "1px solid rgba(0,0,0,.15)";
        });
    }
    // Validations for clockpicker
    var arrStart = start.value.split(':'), hourStart = arrStart[0], minStart = arrStart[1];
    var arrEnd = end.value.split(':'), hourEnd = arrEnd[0], minEnd = arrEnd[1];
    if(((hourEnd < hourStart) || (hourEnd == hourStart && minStart > minEnd)) && start.value !="Choose start time"){
        start.style.border = "1px solid red";
        end.style.border = "1px solid red";
        error += "endBeforeStart ";
        errorMessage.innerHTML += "<br> Endtime cannot be before starttime.";
        $(start).click(function () {
            start.style.border = "1px solid rgba(0,0,0,.15)";
        });
        $(end).click(function () {
            end.style.border = "1px solid rgba(0,0,0,.15)";
        });
    }
    if((hourEnd == hourStart && (minEnd - minStart) < 45) ||
            (hourEnd == +hourStart+1 && (minStart == 30 && minEnd == 0) ||
            (minStart == 45 && minEnd <= 15))){
        start.style.border = "1px solid red";
        end.style.border = "1px solid red";
        error += "tooShort ";
        errorMessage.innerHTML += "<br> Cannot book less than 45min.";
        $(start).click(function () {
            start.style.border = "1px solid rgba(0,0,0,.15)";
        });
        $(end).click(function () {
            end.style.border = "1px solid rgba(0,0,0,.15)";
        });
    }
    if((hourEnd - hourStart) > 3){
        start.style.border = "1px solid red";
        end.style.border = "1px solid red";
        error += "tooLong ";
        errorMessage.innerHTML += "<br> Cannot book more than 3 hours.";
        $(start).click(function () {
            start.style.border = "1px solid rgba(0,0,0,.15)";
        });
        $(end).click(function () {
            end.style.border = "1px solid rgba(0,0,0,.15)";
        });
    }
    if((hourEnd == 22 && minEnd > 0) || (hourStart == 22) || (hourEnd > 22 || 0)){
        start.style.border = "1px solid red";
        end.style.border = "1px solid red";
        error += "tooLate ";
        errorMessage.innerHTML += "<br> Cannot book later than 22:00.";
        $(start).click(function (){
            start.style.border = "1px solid rgba(0,0,0,.15)";
        });
        $(end).click(function (){
            end.style.border = "1px solid rgba(0,0,0,.15)";
        });
    }
    if(hourStart < 10 || hourEnd == 10){
        start.style.border = "1px solid red";
        end.style.border = "1px solid red";
        error += "tooEarly ";
        errorMessage.innerHTML += "<br> Cannot book earlier than 10:00.";
        $(start).click(function (){
            start.style.border = "1px solid rgba(0,0,0,.15)";
        });
        $(end).click(function (){
            end.style.border = "1px solid rgba(0,0,0,.15)";
        });
    }
    if((minEnd != 00 && minEnd != 15 && minEnd != 30 && minEnd != 45) ||
            (minStart != 00 && minStart != 15 && minStart != 30 && minStart != 45)){
        start.style.border = "1px solid red";
        end.style.border = "1px solid red";
        error += "wrongFormat ";
        errorMessage.innerHTML += "<br> Can only book quarter-hourly time periods.";
        $(start).click(function (){
            start.style.border = "1px solid rgba(0,0,0,.15)";
        });
        $(end).click(function (){
            end.style.border = "1px solid rgba(0,0,0,.15)";
        });
    }
    if(error === ""){
        errorMessage.innerHTML = "";
        return true;
    }else {
        return false;
    }
}

