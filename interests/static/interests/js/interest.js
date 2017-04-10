(function(){
  //
  // Module and controllers for Interest-related pages like List and Home views
  //
  var app = angular.module('interest', []);
  var apiBase = '/api/v1';

  app.factory('userFactory', ['$http', function($http){
    var promise = null;
    var userFactory = {};

    userFactory.getUser = function(user_id){
      return $http.get(apiBase + '/user/' + user_id + '/?format=json');
    };

    userFactory.getUserProfile = function(profileid){
      return $http.get(apiBase + '/user_profile/' + profileid + '/?format=json');
    };

    return userFactory;
  }]);

  app.factory('interestFactory', ['$http', function($http){
    var interestFactory = {};

    interestFactory.getAllInterests = function(){
      return $http.get(apiBase + '/interest/?format=json');
    };

    interestFactory.getInterest = function(uri){
      return $http.get(uri + '?format=json');
    };

    interestFactory.buildInterestArray = function(arr){

    };

    return interestFactory;
  }]);


  app.controller('ListController', ['$http', '$log', '$scope', 'interestFactory', function($http, $log, $scope, interestFactory){
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
    interestFactory.getAllInterests().then(function(response){
      $scope.interests = response.data.objects;
      // $log.info($scope.interests);
    });
  }]);


  app.controller('HomeController', ['$http', '$log', '$scope', 'userFactory', 'interestFactory', function($http, $log, $scope, userFactory, interestFactory){
    $scope.userInterestRes = [];  // Array of interest resource URIs
    $scope.userInterests = [];

    userFactory.getUser($scope.uid).then(function(response){
      $scope.userInterestRes = response.data.profile.interests;
      $log.info('User interests ' + $scope.userInterestRes);
      buildInterestArray();
    });

    function buildInterestArray() {
      var len = $scope.userInterestRes.length;
      for (var i = 0; i < len; i++){
        interestFactory.getInterest($scope.userInterestRes[i]).then(function(response){
          $log.info(response.data.news_result.news_items);
          $scope.userInterests.push({
            id: response.data.id,
            title: response.data.title,
            last_refreshed: response.data.last_refreshed,
            news_result: response.data.news_result,
            articles: response.data.news_result.news_items
          });

        });
      }
    }
  }]);

  app.filter('cleanText', function(){
    return function(text){
      if (typeof text != 'string'){
        return text;
      } else {
        text = text.replace(/&apos;/g, '\'').replace(/&quot;/g, '"').replace(/b'/g, '');
        return text;
      }
    }
  });

})();
