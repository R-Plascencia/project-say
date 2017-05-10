(function() {
  //
  // MAIN APP MODULE
  //
  var app = angular.module('sayApp', [
    'ngAnimate',
    'ngRoute',
    'angularUtils.directives.dirPagination',
    'ui.bootstrap',
    'saySidebar',
    'interest'
  ]);
  app.config(['$httpProvider', '$routeProvider', '$locationProvider', function($httpProvider, $routeProvider, $locationProvider) {
      $locationProvider.html5Mode(true);
      $routeProvider
      .when('/', {
        templateUrl: '/static/interests/templates/home.html',
        controller: 'HomeController',
        controllerAs: 'homeCtrl'
      })
      .when('/interests/list',{
        templateUrl: '/static/interests/templates/list.html',
        controller: 'ListController',
        controllerAs: 'listCtrl'
      })
      .when('/about', {
        templateUrl: '/static/sitepages/templates/about.html'
      })
      .otherwise({
        redirectTo: '/'
      });
  }]);
  app.run(['$templateCache', '$route', '$http', function($templateCache, $route, $http){
    var url;
    for (var i in $route.routes){
      if (url = $route.routes[i].templateUrl){
        $http.get(url, {cache: $templateCache});
      }
    }
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
