(function(){
  //
  // Module and controllers for Interest-related pages like List and Home views
  //
  var app = angular.module('interest', []);
  var apiBase = '/api/v1';

  // app.config(['$httpProvider', function($httpProvider) {
  //   $httpProvider.defaults.headers.patch = {
  //       'Content-Type': 'application/json;charset=utf-8'
  //   };
  // }]);

  app.factory('userFactory', ['$http', function($http){
    var promise = null;
    var userFactory = {};

    userFactory.getUser = function(user_id){
      return $http.get(apiBase + '/user/' + user_id + '/?format=json');
    };

    userFactory.getUserProfile = function(profile_id){
      return $http.get(apiBase + '/user_profile/' + profile_id + '/?format=json');
    };

    userFactory.importInterest = function(data_obj, profile_id){
      return $http.patch(apiBase + '/user_profile/' + profile_id + '/', data_obj);
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

    interestFactory.getInterestById = function(id){
      return $http.get(apiBase + '/interest/' + id + '/?format=json');
    };

    interestFactory.updateInterest = function(id, data_obj){
      return $http.patch(apiBase + '/interest/' + id + '/', data_obj);
    };

    return interestFactory;
  }]);


  app.controller('ListController', ['$http', '$log', '$scope', 'interestFactory', 'userFactory', function($http, $log, $scope, interestFactory, userFactory){
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

    this.import = function(int_id){
      var profile_id = 0;
      var user_interests = [];

      // Get the user's user profile ID to start the process
      userFactory.getUser($scope.uid).then(function(response){
        $log.info(response.data.profile.id);
        profile_id = response.data.profile.id;
        getProfileInterests(profile_id);
      });

      // Use user profile to get user's current list of Interests
      function getProfileInterests(profile_id){
        userFactory.getUserProfile(profile_id).then(function(response){
          user_interests = response.data.interests;
          addToInterests(user_interests);
        });
      }

      // Add the importing Interest to the array of current interests for user
      function addToInterests(user_interests){
        interestFactory.getInterestById(int_id).then(function(response){
          user_interests.push(response.data.resource_uri);
          var news_result = response.data.news_result;
          var num_imports = response.data.num_of_imports;
          num_imports += 1;
          sendToPatch(user_interests, profile_id, num_imports, news_result);
        });
      }

      // Contstruct an interests obj to send off to API to PATCH "interests" in profile with new interest
      function sendToPatch(user_interests, profile_id, num_imports, newsresult){
        var dataObj = {
          interests: user_interests
        }
        var intObj = {
          news_result: newsresult,
          num_of_imports: num_imports
        }
        // userFactory.importInterest(dataObj, profile_id).then(function(response){
        //   $log.info('IMPORT SUCCESS');
        // });
        interestFactory.updateInterest(int_id, intObj).then(function(response){
          $log.info('# Imports updated')
        });
      }
    };

    this.isOwned = function(interest_uri){
      if ($scope.userOwnedInterests.indexOf(interest_uri) != -1){
        return true;
      } else {
        return false;
      }
    }

    $scope.interests = [];
    interestFactory.getAllInterests().then(function(response){
      $scope.interests = response.data.objects;
    });

    $scope.userOwnedInterests = [];
    userFactory.getUser($scope.uid).then(function(response){
      $scope.userOwnedInterests = response.data.profile.interests;
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

    // Build the Array of attributes for each Interest to display in the home page
    function buildInterestArray() {
      var len = $scope.userInterestRes.length;
      for (var i = 0; i < len; i++){
        interestFactory.getInterest($scope.userInterestRes[i]).then(function(response){
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
