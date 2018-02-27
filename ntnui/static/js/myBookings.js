
//Popup for editing a booking

function myBookingEdit() {
    //popup elements
    var popupTag = document.createElement("div");
    var popupContent = document.createElement("div");
    var popupSpan = document.createElement("span");
    var popupInfo = document.createElement("h1");
    popupTag.className = "modal-large";
    popupContent.className = "modal-content";
    popupContent.appendChild(popupSpan);
    popupContent.appendChild(popupInfo);
    popupTag.appendChild(popupContent);
    popupTag.id = "popupTest";
    popupSpan.id = "popupSpan";

    document.body.appendChild(popupTag);
    var modal = document.getElementById(popupTag.id);
    var btn = document.getElementById("editButton");
    var span = document.getElementById(popupSpan.id);
    //popupContent.appendChild(popupInfo);
    btn.onclick = function() {
        modal.style.display = "block";
        $(".modal-content").load("delete/3");

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
    }}


//Popup for deleting a booking
function myBookingDelete() {
    //popup elements
    var popupTag = document.createElement("div");
    var popupContent = document.createElement("div");
    var popupSpan = document.createElement("span");
    var popupInfo = document.createElement("h1");
    popupTag.className = "modal-large";
    popupContent.className = "modal-content";
    popupContent.appendChild(popupSpan);
    popupContent.appendChild(popupInfo);
    popupTag.appendChild(popupContent);
    popupTag.id = "popupTest";
    popupSpan.id = "popupSpan";

    document.body.appendChild(popupTag);
    var modal = document.getElementById(popupTag.id);
    var btn = document.getElementById("deleteButton");
    var span = document.getElementById(popupSpan.id);
    //popupContent.appendChild(popupInfo);
    btn.onclick = function() {
        modal.style.display = "block";
        $(".modal-content").load("delete/3");

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
    }}



myBookingEdit();
myBookingDelete();