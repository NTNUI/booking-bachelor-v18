$(document).on('click', '.deleteModal', function(e){
    deleteModal(e);
});


//Popup for deleting a booking
function deleteModal(e) {
    $('.booking-modal-contents').load('delete/'+(e.target.id));

    //Set global tempDay variable to event that triggers the popup, ie the date.
    var modal = document.getElementById('booking-modal');
    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];
    modal.style.display = "block";

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

