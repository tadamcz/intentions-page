// JQuery
$(document).ready(function() {

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

// Mousetrap
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

    console.log(has_focus)
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
    $('.create_intention input#title').focus()
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

var create_form = $('.create_intention form').get(0)
Mousetrap(create_form).bind('esc', function (e){ // override above binding of 'esc' for this specific case
    $(create_form).find('input').blur()
})

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

});
