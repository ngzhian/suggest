(function($){
$(function() {
var $content = $('#content');
$content.on('keyup', function(e) {
    e.stopPropagation();
    console.log('keyup');
})
});
}(window.jQuery))
