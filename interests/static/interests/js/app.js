(function() {

  var app = angular.module('sayApp', [
    'ngAnimate',
    'angularUtils.directives.dirPagination',
    'ui.bootstrap',
    'saySidebar'
  ]);
  app.config(function($httpProvider) {
      $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
  });

  // // Avoid Django and NG template tag collision
  // app.config(function($interpolateProvider){
  //   $interpolateProvider.startSymbol('{$');
  //   $interpolateProvider.endSymbol('$}');
  // });

  app.controller('CreationController', function(){
    this.interest = {};
    this.btnClicked = false;
    this.createOnly = false;
  });

  app.controller('listController', ['$http', '$log', '$scope', function($http, $log, $scope){
    this.sortType = 'imports';
    this.sortReverse = false;
    this.searchInterests = '';
    this.btnClicked = false;

    this.setSortType = function(sortType){
      this.sortType = sortType;
    };

    this.isSortedBy = function(sortType){
      return this.sortType === sortType;
    };

    this.toggleSortReverse = function(){
      this.sortReverse = !this.sortReverse;
    };

    $scope.interests = [];
    $http.get('/api/v1/interest/?format=json').then(function(response){
      $scope.interests = response.data.objects;
      $log.info($scope.interests);
    });


  }]);

  app.filter('anyInvalidDirtyFields', function () {
    return function(form) {
      for(var prop in form) {
        if(form.hasOwnProperty(prop)) {
          if(form[prop].$invalid && form[prop].$dirty) {
            return true;
          }
        }
      }
      return false;
    };
  });


})();
