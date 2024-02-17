
// Listen for click on toggle checkbox
$('#select-all').click(function(event) {   
    if(this.checked) {
        // Iterate each checkbox
        $('.subfolders :checkbox').each(function() {
            this.checked = true;                        
        });
    } else {
        $('.subfolders :checkbox').each(function() {
            this.checked = false;                       
        });
    }
}); 
