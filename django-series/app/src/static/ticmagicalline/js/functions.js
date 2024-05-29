document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var instances = M.Sidenav.init(elems, []);
});

function play(id, movement) {
    window.location.href = "/play/"+id+"/move/"+movement;
}