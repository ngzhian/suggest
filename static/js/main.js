(function($){
$(function() {
var $content = $('#content');
$content.on('keyup', function(e) {
    e.stopPropagation();
    // get current article
    // send current context to server endpoint
    // call api to get classification
    // using results from classification call content api
    // write conten to sidbar
});
// var $button = $('#submit');
// $button.on('click', function() {
//     $.post('suggest/', {
//         'content': $content.val().trim(),
//         'current': $content.val().trim(),
//     })
//     .done(function(res) {
//         var $related = $('#related');
//         var articles = res.result;
//         $.each(articles, function(i, v) {
//             var headline = v.headline.main || '',
//                 snippet = v.snippet || '',
//                 pub_date = v.pub_date || '',
//                 section_name = v.section_name || '',
//                 url = v.web_url,
//                 keywords = $.map(v.keywords, function(keyword) {
//                     if (keyword.is_major !== 'Y') {
//                         return null;
//                     }
//                     return keyword.value;
//                 }) || [];
//             var content = Array.join([headline, snippet, pub_date, section_name,
//                 Array.join(keywords, ',')], ':')
//             $related.append('<p>' + content + '</p>')
// //append to related
//         });
//     })
//     .fail(function(res) {
//         console.log(res.err);
//     });
// });
});
}(window.jQuery))
