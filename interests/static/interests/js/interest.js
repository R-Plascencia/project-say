(function(){
  //
  // Module and controllers for Interest-related pages like List and Home views
  //
  var app = angular.module('interest', []);

  app.factory('userProfileFactory', ['$http', function($http, $scope){
    var promise = null;
    var userProfileFactory = {};

    userProfileFactory.getInterestURIs = function(profileid){
      return $http.get('/api/v1/user_profile/' + profileid + '/?format=json');
    };

    return userProfileFactory;
  }]);


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


  app.controller('HomeController', ['$http', '$log', '$scope', 'userProfileFactory', function($http, $log, $scope, userProfileFactory){
    $scope.userInterests = [];
    // $http.get('/api/v1/user_profile/' + $scope.profileid + '/?format=json').then(function(response){
    //   $log.info($scope.profileid);
    //   $scope.userInterests = response.data.interests;
    //   $log.info($scope.userInterests);
    // });
    userProfileFactory.getInterestURIs($scope.profileid).then(function(response){
      $log.info('URIs of user intersts are ' + response.data.interests);
    });

  }]);

})();
