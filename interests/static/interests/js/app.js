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
  app.config(function($httpProvider, $routeProvider, $locationProvider) {
      $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
      $locationProvider.html5Mode(true);
      $routeProvider
      .when('/', {
        templateUrl: '/static/interests/views/home.html',
        controller: 'HomeController',
        controllerAs: 'homeCtrl'
      });
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
