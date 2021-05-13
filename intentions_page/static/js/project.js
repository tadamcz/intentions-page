// JQuery
$(document).ready(function() {

// Avoid multiple form submissions by disabling forms on submit
$(".form-disable-on-submit").on('submit', function (event){
    var form = event.target
    var submitButton = $(form).find("button[type='submit']")
    submitButton.attr('disabled',true)
    submitButton.text('Wait...')
})

// Cmd-Enter to submit on multi-line form
$('.create_intention form').keydown(function(event) {
    if ((event.ctrlKey || event.metaKey) && event.keyCode === 13) {
      $(this).submit();
    }
})

// uses third-party 'autosize' library
autosize($('.create_intention textarea'));
autosize($('.notesEditForm textarea'))



// Handle keyboard focus on intentions
function getFocusFromLocalStorage() {
    var keyboard_nav_active = localStorage.getItem('keyboard_nav_active')

    if (keyboard_nav_active) {
        var has_focus_id = localStorage.getItem('has_keyboard_focus')
        if (has_focus_id) {
            has_focus = $('#' + localStorage.getItem('has_keyboard_focus'))
            has_focus.attr('has_keyboard_focus', '1')
            return has_focus
        }
    }
    return false
}

getFocusFromLocalStorage()

function getNextIntention(has_focus) {
    var found = false
    $('.intention').each( function (){
        if (found) {
            found = $(this)
            return false // breaks out of .each()
        }
        if ($(this).is(has_focus)) {found = $(this)}
        }
    )
    return found
}

function getPrevIntention(has_focus) {
    var found = false
    $($('.intention').get().reverse()).each( function (){
        if (found) {
            found = $(this)
            return false // breaks out of .each()
        }
        if ($(this).is(has_focus)) {found = $(this)}
        }
    )
    return found

}

function setKeyboardFocus(intention){
    intention.attr('has_keyboard_focus', '1')
    localStorage.setItem('has_keyboard_focus',intention.attr('id'))
    localStorage.setItem('keyboard_nav_active','1')
}

// Bind shortcuts using 'Moustrap' library
Mousetrap.bind('t', function (e){
    window.location.assign('/')
})

Mousetrap.bind('h', function (e){
    window.location.assign('/history')
})

Mousetrap.bind('j', function(e) {
    var has_focus = $('.intention_list').find('[has_keyboard_focus]')

    if (!has_focus.length) {
        has_focus = getFocusFromLocalStorage()
    }

    if (has_focus.length) {
        var next = getNextIntention(has_focus)
        if (next.length) {
            has_focus.removeAttr('has_keyboard_focus')
            setKeyboardFocus(next)
        }
    } else {
        var intention = $('.intention_list').find('.intention').first()
        setKeyboardFocus(intention)
    }
})

Mousetrap.bind('k', function(e) {
    var has_focus = $('.intention_list').find('[has_keyboard_focus]')

    if (!has_focus.length) {
        has_focus = getFocusFromLocalStorage()
    }

    if (has_focus.length) {
        var prev = getPrevIntention(has_focus)
        if (prev.length) {
            has_focus.removeAttr('has_keyboard_focus')
            setKeyboardFocus(prev)
        }
    } else {
        var intention = $('.intention_list').find('.intention').first()
        setKeyboardFocus(intention)
    }
})

Mousetrap.bind('n', function (e){
    $('#intentionCreateField').focus()
    e.preventDefault()
})

Mousetrap.bind('esc', function (e) {
    if ($('body').hasClass('modal-open')) {
        return
    }

    var has_focus = $('.intention_list').find('[has_keyboard_focus]')
    if (has_focus.length){
        has_focus.removeAttr('has_keyboard_focus')
        localStorage.setItem('keyboard_nav_active','')
    }
})

var textareas = $('.notesEditForm textarea, .create_intention textarea').each(function (i, e) { // override above binding of 'esc' for this specific case
        Mousetrap(e).bind('esc', function (e){
            e.target.blur()
        })

    }

)


Mousetrap.bind(['space','x'], function (e) {
    var has_focus = $('.intention_list').find('[has_keyboard_focus]')
    if (has_focus.length){
        e.preventDefault()
    }
    has_focus.find('input#id_completed').click()
})

Mousetrap.bind('a', function (e) {
    var has_focus = $('.intention_list').find('[has_keyboard_focus]')
    if (has_focus.length){
        has_focus.find('.append_button').click()
    }
})

$('.appendTextModal').on('shown.bs.modal', function (e) {
    $(this).find('.append_field').focus()
})

Mousetrap.bind('f', function (e) {
    var has_focus = $('.intention_list').find('[has_keyboard_focus]')
    if (has_focus.length){
        has_focus.find('.nevermind_button').click()
    }
})

Mousetrap.bind('?', function (e) {
    $('#keyboardShortcutModal').modal('toggle')
})

// Feedback form
$("#feedbackForm").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = form.attr('action');

    $.ajax({
           type: "POST",
           url: url,
           data: form.serialize(), // serializes the form's elements.
           success: function(data)
           {
               $('#feedbackCallback').text('Success. Thanks for the feedback.').css('color','green')
           },
           error: function(data){
               $('#feedbackCallback').text('Failed. Try emailing me instead: tmkadamcz@gmail.com').css('color','red')
           }
         });
});

function SendFormAJAX(form){ // returns a function
    return function (){
        var versionField = form.find("input[name='version']")
        versionField.val(function(i, oldval){
            return parseInt(oldval)+1
        })
        $.ajax({
            type: form.attr('method').toUpperCase(),
            url: form.attr('action'),
            data: form.serialize(),
            beforeSend: function (){
                form.find('.notesFieldSaveCallback').text('Autosaving...')
            },
            success: function (){
                form.find('.notesFieldSaveCallback').text('Autosaved')
            }
      });}
}

$('.notesEditForm').each(function (index, element){
    var form = $(element)
    var ajaxThrottled = _.throttle(SendFormAJAX(form), 500)
    form.on("input", ajaxThrottled)
})

$('.collapseNotes')
    .on('shown.bs.collapse', function (){
        $(this).find('textarea').focus()
    })
    .on('hidden.bs.collapse', function (){
    $(this).find('textarea').blur()
})

}); // JQuery Close
