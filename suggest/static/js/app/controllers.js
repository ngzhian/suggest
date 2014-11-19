'use strict';

/* Controllers */

var suggestApp = angular.module('suggestApp', ['suggestAnimations', 'components']);

suggestApp.controller('relatedCtrl', ['$scope', '$http',
    function($scope, $http) {
        $scope.getRelated = function(content) {
            var content = $('#content');
            if (!$scope.entities) {
                $scope.getEntity(content.val().trim())
            }
            // still need the actual DOM to get selectionStart and selectionEnd
            $http.post('suggest/', {
                content: content.val().trim(),
            }).success(function(data, status, headers, config) {
                var articles = data.result;
                var related = articles.map(function(v) {
                    var headline = v.headline.main || '',
                        snippet = v.snippet || '',
                        pub_date = v.pub_date || '',
                        section_name = v.section_name || '',
                        keywords_list = v.keywords_list || '',
                        url = v.url;
                    return {
                        'headline': headline,
                        'snippet': snippet,
                        'pub_date': pub_date,
                        'section_name': section_name,
                        'url': url,
                        'keywords_list': keywords_list,
                    }
                });
                $scope.related = related;
                var keywords = data.keywords;
                $scope.keywords = keywords;
            });
        };
        $scope.getEntity = function(content) {
            $scope.tooShort = false;
            if (!content) {
                return;
            }
            $http.post('entity/', {
                content: content.trim()
            }).success(function(data, status, headers, config) {
                $scope.entities = data.result;
            });
 
        };
        $scope.addLink = function(url, headline) {
            var content = $('#content'),
                open_tag = ' <a href="' + url + '" title="' + headline + '">',
                close_tag = '</a>',
                start = content[0].selectionStart,
                end = content[0].selectionEnd,
                text = content.val();
            // special case when start is 0
            // another special case when end is 0, TODO
            if (start === text.length && start > 0) {
                start--;
            }
            while (start > 0 & start < text.length && !text[start].match(/\s/)) {
                start--;
            }
            if (end === 0 && start > 0) {
                start--;
            }
            if (end > 1 && text[end-1].match(/\s/)) {
                // when user double clicks on text, the selection ends on a whitespace
                end--;
            }
            while (end > 0 && end < text.length && !text[end].match(/\s/)) {
                end++;
            }
            var start_text = text.slice(0, start),
                mid_text = text.slice(start, end),
                end_text = text.slice(end, text.length),
                new_text = [start_text, open_tag, mid_text, close_tag, end_text].join('');
            content.val(new_text);
        };
        $scope.keyup = function(event) {
            window.clearTimeout($scope.timeoutID);
            $scope.timeoutID = window.setTimeout(function() { $scope.getEntity($scope.content) }, 3000);
            // alt ctrl 1 
            if (event.altKey && event.ctrlKey) {
                event.stopImmediatePropagation();
                // when user press 1, expect to insert link for first article
                // key 1 is 49 and index starts from 0
                var num = parseInt(event.which, 10) - 48 - 1;
                if ($scope.related && num < $scope.related.length) {
                    var to_insert = $scope.related[num];
                    $scope.addLink(to_insert.url, to_insert.headline);
                }
            }
        };
    }
]);
