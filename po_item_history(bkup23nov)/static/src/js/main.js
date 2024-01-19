$(document).ready(function() {
$('table').on('scroll', function () {
    $("table > *").width($("table").width() + $("table").scrollLeft());
});
});
