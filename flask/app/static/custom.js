function activateModal(elId) {
    var modalEl = document.getElementById(elId);

    // initialize modal element
    var modalEl = document.createElement('div');
    modalEl.className = 'modal';

    modalEl.innerHTML = document.getElementById(elId).outerHTML;

    // show modal
    mui.overlay('on', modalEl);
}

Behavior2.Class('formfill', 'form', {
    reset: {
        'form': 'reset'
    }
}, function($ctx, that) {
    that.reset = function(evt) {
        $ctx.find('button[type="submit"]').button('reset');
        return $ctx.values($ctx.data('vars'));
    };
    $ctx.values($ctx.data('vars'));
    $ctx.errors($ctx.data('errors'));
    $ctx.data('initialized', true);
    return $ctx.trigger('initialized');
});
