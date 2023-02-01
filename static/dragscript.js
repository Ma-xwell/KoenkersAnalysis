// Function allowing to sort items on the webpage
// It also tracks their current position and updates the array with positions order
$(document).ready(function(){
    $(function() {
        $(".items").sortable({
            update: function (event, ui) {
                var sortedIDs = $(this).sortable("toArray");
                var sortedStringified = JSON.stringify(sortedIDs)
                // Preventing website from scrolling up when updating the sortable elements
                jQuery(this).height(jQuery(this).height());
                // Updating the array to have new order of elements
                document.getElementById("rankingarray").value = sortedStringified;
                
                // TEST
                $("#testID").text(sortedIDs.toString());
            }
        });
    });
    
});