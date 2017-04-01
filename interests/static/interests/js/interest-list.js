(function(){
  var app = angular.module('interest-list', ['ngAnimate', 'angularUtils.directives.dirPagination', 'ui.bootstrap']);

  app.directive('interestList', ['$http', '$log', '$scope', function(){
    return {
      restrict: 'E',
      templateUrl: 'interest-list.html',
      controller: function($http, $log, $scope){
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
      }],
      controllerAs: 'listCtrl',
    };
  }]);

})();
