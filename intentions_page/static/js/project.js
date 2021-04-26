/* Project specific Javascript goes here. */
$(document).ready(function() {

// Append functionality
$('.append_button').click( function(event) {
    var button = $(event.target)
    var append_field = button.closest(".intention").find('.append_field')
    var message = window.prompt('What to append?')
    append_field.attr('value',message)
    append_field.closest('form').submit()
    }
)

})
