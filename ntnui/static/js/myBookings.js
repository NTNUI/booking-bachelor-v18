
/* Call delete modal when clicked */
$(document).on('click', '.deleteModal', function(e){
    deleteModal(e);
});

/* Open modal with correct content */
function deleteModal(e) {
    $('.booking-modal-contents').load('delete/'+(e.target.id));

    //Set global tempDay variable to event that triggers the popup, ie the date.
    var modal = document.getElementById('booking-modal');
    modal.style.display = "block";

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
}

/* Call delete modal when clicked */
$(document).on('click', '.editModal', function(e){
    editModal(e);
});

/* Open modal with correct content */
function editModal(e) {
    $('.booking-modal-contents').load('edit/'+(e.target.id));

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