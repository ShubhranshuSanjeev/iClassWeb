document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.sidenav');
    var elems1 = document.querySelectorAll('.collapsible')
    var elems2 = document.querySelectorAll('.modal');
    var instances = M.Sidenav.init(elems, []);
    var instances1 = M.Collapsible.init(elems1, []);
    var instances2 = M.Modal.init(elems2, []);
});
function loadAssignmentNumber(n){
    document.getElementById('id_assignmentId').value = parseInt(n);
}
function loadStudent(n){
    document.getElementById('studId').value = n;
    console.log(document.getElementById('studId').value)
}