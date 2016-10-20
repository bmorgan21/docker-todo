function activateModal(elId) {
    var modalEl = document.getElementById(elId);

    // initialize modal element
    var modalEl = document.createElement('div');
    modalEl.className = 'modal';

    modalEl.innerHTML = document.getElementById(elId).outerHTML;

    // show modal
    mui.overlay('on', modalEl);
}
