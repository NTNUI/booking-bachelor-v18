// Validation for the form

function validateForm(){
    var description = document.forms["createform"]["id_description"];
    var title = document.forms["createform"]["id_title"];
    var start = document.forms["createform"]["startInput"];
    var end = document.forms["createform"]["endInput"];
    var error = "";
    if(description.value === ""){
        description.style.border = "1px solid red";
        error += "description ";
        $(description).click(function (){
            description.style.border = "1px solid rgba(0,0,0,.15)";
        })
    }
    if(title.value === ""){
        title.style.border = "1px solid red";
        error += "title ";
        $(title).click(function (){
            title.style.border = "1px solid rgba(0,0,0,.15)";
        })
    }
    if(start.value === "Choose start time"){
        start.style.border = "1px solid red";
        error += "start ";
        $(start).click(function (){
            start.style.border = "1px solid rgba(0,0,0,.15)";
        })
    }
    if(end.value === "Choose end time"){
        end.style.border = "1px solid red";
        error += "end ";
        $(end).click(function (){
            end.style.border = "1px solid rgba(0,0,0,.15)";
        })
    }
    // Validation for time-picker
    var arrStart = start.value.split(':'), hourStart = arrStart[0], minStart = arrStart[1];
    var arrEnd = end.value.split(':'), hourEnd = arrEnd[0], minEnd = arrEnd[1];
    if(((hourEnd < hourStart) || (hourEnd == hourStart && minStart > minEnd)) ||
            ((hourEnd == 22 && minEnd > 0) || (hourStart == 22) || (hourEnd > 22 || 0) || (hourStart < 10)) ||
            ((hourEnd-hourStart)>3) ||
            (hourEnd==hourStart && (minEnd - minStart)<30)){
        start.style.border = "1px solid red";
        end.style.border = "1px solid red";
        error += "start ";
        error += "end ";
        $(start).click(function () {
            start.style.border = "1px solid rgba(0,0,0,.15)";
        });
        $(end).click(function () {
            end.style.border = "1px solid rgba(0,0,0,.15)";
        })
    }
    return(error === "");
}

