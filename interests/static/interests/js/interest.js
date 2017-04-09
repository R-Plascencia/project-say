(function(){
  //
  // Module and controllers for Interest-related pages like List and Home views
  //
  var app = angular.module('interest', []);

  app.factory('userFactory', ['$http', function($http, $scope){
    var promise = null;
    var userFactory = {};

    userFactory.getUser = function(user_id){
      return $http.get('/api/v1/user/' + user_id + '/?format=json');
    };

    return userFactory;
  }]);


  app.controller('ListController', ['$http', '$log', '$scope', function($http, $log, $scope){
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


  app.controller('HomeController', ['$http', '$log', '$scope', 'userFactory', function($http, $log, $scope, userFactory){
    $scope.userInterests = [];
    // $http.get('/api/v1/user_profile/' + $scope.profileid + '/?format=json').then(function(response){
    //   $log.info($scope.profileid);
    //   $scope.userInterests = response.data.interests;
    //   $log.info($scope.userInterests);
    // });
    userFactory.getUser($scope.uid).then(function(response){
      $log.info('URIs of user intersts are ' + response.data.profile.interests);
    });

  }]);

})();
